def get_sonarqube_unresolved_issues(report_task_file){
    script{
        if(! fileExists(report_task_file)){
            error "Could not find ${report_task_file}"
        }
        def props = readProperties  file: report_task_file
        if(! props['serverUrl'] || ! props['projectKey']){
            error "Could not find serverUrl or projectKey in ${report_task_file}"
        }
        def response = httpRequest url : props['serverUrl'] + '/api/issues/search?componentKeys=' + props['projectKey'] + '&resolved=no'
        def outstandingIssues = readJSON text: response.content
        return outstandingIssues
    }
}

def getPypiConfig() {
    node(){
        configFileProvider([configFile(fileId: 'pypi_config', variable: 'CONFIG_FILE')]) {
            def config = readJSON( file: CONFIG_FILE)
            return config['deployment']['indexes']
        }
    }
}

def createWindowUVConfig(){
    def scriptFile = "ci\\scripts\\new-uv-global-config.ps1"
    if(! fileExists(scriptFile)){
        checkout scm
    }
    return powershell(
        label: 'Setting up uv.toml config file',
        script: "& ${scriptFile} \$env:UV_INDEX_URL \$env:UV_EXTRA_INDEX_URL",
        returnStdout: true
    ).trim()
}

def createUnixUvConfig(){

    def scriptFile = 'ci/scripts/create_uv_config.sh'
    if(! fileExists(scriptFile)){
        checkout scm
    }
    return sh(label: 'Setting up uv.toml config file', script: "sh ${scriptFile} " + '$UV_INDEX_URL $UV_EXTRA_INDEX_URL', returnStdout: true).trim()
}

def call(){
    library(
        identifier: 'JenkinsPythonHelperLibrary@2024.12.0',
        retriever: modernSCM(
            [
                $class: 'GitSCMSource',
                remote: 'https://github.com/UIUCLibrary/JenkinsPythonHelperLibrary.git'
            ]
        )
    )
    pipeline {
        agent none

        options {
            buildDiscarder logRotator(artifactDaysToKeepStr: '10', artifactNumToKeepStr: '10')
        }
        parameters {
            string(name: 'PROJECT_NAME', defaultValue: 'Hathi Validate', description: 'Name given to the project')
            booleanParam(name: 'RUN_CHECKS', defaultValue: true, description: 'Run checks on code')
            booleanParam(name: 'USE_SONARQUBE', defaultValue: true, description: 'Send data test data to SonarQube')
            booleanParam(name: 'TEST_RUN_TOX', defaultValue: false, description: 'Run Tox Tests')
            booleanParam(name: 'BUILD_PACKAGES', defaultValue: false, description: 'Build Python packages')
            booleanParam(name: 'INCLUDE_LINUX-ARM64', defaultValue: false, description: 'Include ARM architecture for Linux')
            booleanParam(name: 'INCLUDE_LINUX-X86_64', defaultValue: true, description: 'Include x86_64 architecture for Linux')
            booleanParam(name: 'INCLUDE_MACOS-ARM64', defaultValue: false, description: 'Include ARM(m1) architecture for Mac')
            booleanParam(name: 'INCLUDE_MACOS-X86_64', defaultValue: false, description: 'Include x86_64 architecture for Mac')
            booleanParam(name: 'INCLUDE_WINDOWS-X86_64', defaultValue: true, description: 'Include x86_64 architecture for Windows')
            booleanParam(name: 'TEST_PACKAGES', defaultValue: true, description: 'Build Python packages')
            credentials(name: 'SONARCLOUD_TOKEN', credentialType: 'org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl', defaultValue: 'sonarcloud_token', required: false)
            booleanParam(name: 'DEPLOY_PYPI', defaultValue: false, description: 'Deploy to pypi')
            booleanParam(name: 'DEPLOY_HATHI_TOOL_BETA', defaultValue: false, description: 'Deploy standalone to \\\\storage.library.illinois.edu\\HathiTrust\\Tools\\beta\\')
            booleanParam(name: 'DEPLOY_DOCS', defaultValue: false, description: 'Update online documentation')
        }
        stages {
            stage('Building and Testing'){
                when{
                    anyOf{
                        equals expected: true, actual: params.RUN_CHECKS
                        equals expected: true, actual: params.TEST_RUN_TOX
                        equals expected: true, actual: params.DEPLOY_DOCS
                    }
                }
                stages{
                    stage('Build Documentation'){
                        agent {
                            docker{
                                image 'ghcr.io/astral-sh/uv:debian'
                                label 'docker && linux && x86_64' // needed for pysonar-scanner which is x86_64 only as of 0.2.0.520
                                 args '--mount source=python-tmp-hathivalidate,target=/tmp --tmpfs /.local/share:exec --tmpfs /venv:exec -e UV_PROJECT_ENVIRONMENT=/venv'
                            }
                        }
                        environment{
                            PIP_CACHE_DIR='/tmp/pipcache'
                            UV_TOOL_DIR='/tmp/uvtools'
                            UV_PYTHON_CACHE_DIR='/tmp/uvpython'
                            UV_CACHE_DIR='/tmp/uvcache'
                            UV_PYTHON='3.12'
                            UV_CONFIG_FILE=createUnixUvConfig()
                            UV_FROZEN='1'
                        }
                        options {
                            retry(3)
                        }
                        when{
                            anyOf{
                                equals expected: true, actual: params.RUN_CHECKS
                                equals expected: true, actual: params.DEPLOY_DOCS
                            }
                            beforeAgent true
                        }
                        steps{
                            catchError(buildResult: 'UNSTABLE', message: 'Building documentation produced an error or a warning', stageResult: 'UNSTABLE') {
                                sh(script: 'uv run --no-dev --group docs sphinx-build -b html docs/source build/docs/html -d build/docs/doctrees -w logs/build_sphinx.log -W --keep-going'
                                )
                            }
                        }
                        post{
                            always {
                                recordIssues(tools: [sphinxBuild(name: 'Sphinx Documentation Build', pattern: 'logs/build_sphinx.log')])
                                archiveArtifacts artifacts: 'logs/build_sphinx.log', allowEmptyArchive: true
                                script{
                                    def props = readTOML( file: 'pyproject.toml')['project']
                                    zip archive: true, dir: 'build/docs/html', glob: '', zipFile: "dist/${props.name}-${props.version}.doc.zip"
                                    stash includes: 'dist/*.doc.zip,build/docs/html/**', name: 'DOCUMENTATION'
                                }
                            }
                            success{
                                publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'build/docs/html', reportFiles: 'index.html', reportName: 'Documentation', reportTitles: ''])
                            }
                            cleanup{
                                sh 'git clean -dfx'
                            }
                        }
                    }
                    stage('Checks') {
                        when{
                            equals expected: true, actual: params.RUN_CHECKS
                        }
                        environment{
                            UV_PYTHON='3.12'
                            UV_FROZEN='1'
                        }
                        stages{
                            stage('Code Quality'){
                                agent {
                                    docker{
                                        image 'ghcr.io/astral-sh/uv:debian'
                                        label 'docker && linux && x86_64'
                                        args '--mount source=python-tmp-hathivalidate,target=/tmp --tmpfs /.local/share:exec --tmpfs /.config:exec --tmpfs /venv:exec -e UV_PROJECT_ENVIRONMENT=/venv --tmpfs /.tree-sitter:exec'
                                    }
                                }
                                environment{
                                    PIP_CACHE_DIR='/tmp/pipcache'
                                    UV_TOOL_DIR='/tmp/uvtools'
                                    UV_PYTHON_CACHE_DIR='/tmp/uvpython'
                                    UV_CACHE_DIR='/tmp/uvcache'
                                    UV_CONFIG_FILE=createUnixUvConfig()
                                }
                                stages{
                                    stage('Setup Testing Environment'){
                                        options {
                                            retry(3)
                                        }
                                        steps{
                                            sh(
                                                label: 'Create virtual environment',
                                                script: 'uv sync --frozen --group ci'
                                                       )
                                            sh(label: 'Adding logs and reports directories',
                                               script: '''
                                                    mkdir -p logs
                                                    mkdir -p reports
                                                    '''
                                               )
                                        }
                                        post{
                                            failure{
                                                cleanWs(
                                                    patterns: [
                                                        [pattern: 'uv.toml', type: 'INCLUDE'],
                                                        [pattern: '.venv', type: 'INCLUDE'],
                                                        [pattern: 'bootstrap_uv', type: 'INCLUDE'],
                                                    ]
                                                )
                                            }
                                        }
                                    }
                                    stage('Running Tests') {
                                        parallel {
                                            stage('PyTest'){
                                                steps{
                                                    sh(
                                                        label: 'Running pytest',
                                                        script: 'uv run coverage run --parallel-mode --source=src -m pytest --junitxml=./reports/pytest-junit.xml -p no:cacheprovider'
                                                    )

                                                }
                                                post {
                                                    always{
                                                        junit 'reports/pytest-junit.xml'
                                                    }
                                                }
                                            }
                                            stage('MyPy'){
                                                steps{
                                                    catchError(buildResult: 'SUCCESS', message: 'MyPy found issues', stageResult: 'UNSTABLE') {
                                                        sh(label: 'Running MyPy',
                                                           script: 'uv run mypy -p hathi_validate --html-report reports/mypy_html --cache-dir=/dev/null > logs/mypy.log'
                                                          )
                                                    }
                                                }
                                                post{
                                                    always {
                                                        publishHTML([allowMissing: true, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'reports/mypy_html', reportFiles: 'index.html', reportName: 'MyPy', reportTitles: ''])
                                                        recordIssues tools: [myPy(pattern: 'logs/mypy.log')]
                                                    }
                                                }
                                            }
                                            stage('Flake8') {
                                                steps{
                                                    catchError(buildResult: 'SUCCESS', message: 'flake8 found some warnings', stageResult: 'UNSTABLE') {
                                                        sh(label: 'Running flake8',
                                                           script: 'uv run flake8 src --tee --output-file=logs/flake8.log'
                                                        )
                                                    }
                                                }
                                                post {
                                                    always {
                                                        recordIssues(tools: [flake8(name: 'Flake8', pattern: 'logs/flake8.log')])
                                                    }
                                                }
                                            }
                                            stage('Task Scanner'){
                                                steps{
                                                    recordIssues(tools: [taskScanner(highTags: 'FIXME', includePattern: 'src/hathi_validate/**/*.py', normalTags: 'TODO')])
                                                }
                                            }
                                            stage('Audit Lockfile Dependencies'){
                                                steps{
                                                    catchError(buildResult: 'UNSTABLE', message: 'uv-secure found issues', stageResult: 'UNSTABLE') {
                                                        sh 'uv run --only-group=audit-dependencies --frozen --isolated uv-secure --disable-cache uv.lock'
                                                    }
                                                }
                                            }
                                            stage('Behave') {
                                                steps {
                                                    catchError(buildResult: 'UNSTABLE', message: 'Did not pass all Behave BDD tests', stageResult: 'UNSTABLE') {
                                                        sh(
                                                            script: 'uv run coverage run --parallel-mode --source=src -m behave --junit --junit-directory reports/tests/behave'
                                                        )
                                                    }
                                                }
                                                post {
                                                    always {
                                                        junit 'reports/tests/behave/*.xml'
                                                    }
                                                }
                                            }
                                            stage('pyDocStyle'){
                                                steps{
                                                    catchError(buildResult: 'SUCCESS', message: 'pyDocStyle found issues', stageResult: 'UNSTABLE') {
                                                        tee("reports/pydocstyle-report.txt"){
                                                            sh(
                                                                label: 'Run pydocstyle',
                                                                script: 'uv run pydocstyle src/hathi_validate'
                                                            )
                                                        }
                                                    }
                                                }
                                                post {
                                                    always{
                                                        recordIssues(tools: [pyDocStyle(pattern: 'reports/pydocstyle-report.txt')])
                                                    }
                                                }
                                            }
                                            stage('Pylint') {
                                                steps{
                                                    catchError(buildResult: 'SUCCESS', message: 'Pylint found issues', stageResult: 'UNSTABLE') {
                                                        tee('reports/pylint.txt'){
                                                            sh(label: 'Running pylint',
                                                                script: 'uv run pylint hathi_validate -r n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" --persistent=no'
                                                            )
                                                        }
                                                    }
                                                    sh(
                                                        label: 'Running pylint for sonarqube',
                                                        script: 'uv run pylint hathi_validate -r n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" --persistent=no > reports/pylint_issues.txt',
                                                        returnStatus: true
                                                    )
                                                }
                                                post{
                                                    always{
                                                        recordIssues(tools: [pyLint(pattern: 'reports/pylint.txt')])
                                                    }
                                                }
                                            }
                                            stage('Doctest'){
                                                steps{
                                                    sh 'uv run -m sphinx -b doctest docs/source build/docs -d build/docs/doctrees -v'
                                                }

                                            }
                                        }
                                        post{
                                            always{
                                                sh(label: 'Combining Coverage Data',
                                                   script: '''uv run coverage combine
                                                              uv run coverage xml -o ./reports/coverage.xml
                                                           '''
                                                )
                                                recordCoverage(tools: [[parser: 'COBERTURA', pattern: 'reports/coverage.xml']])
                                            }
                                        }
                                    }
                                    stage('Run Sonarqube Analysis'){
                                        options{
                                            lock('hathivalidate-sonarscanner')
                                        }
                                        environment{
                                            VERSION="${readTOML( file: 'pyproject.toml')['project'].version}"
                                            SONAR_USER_HOME='/tmp/sonar'
                                        }
                                        when{
                                            allOf{
                                                equals expected: true, actual: params.USE_SONARQUBE
                                                expression{
                                                    try{
                                                        withCredentials([string(credentialsId: params.SONARCLOUD_TOKEN, variable: 'dddd')]) {
                                                            echo 'Found credentials for sonarqube'
                                                        }
                                                    } catch(e){
                                                        return false
                                                    }
                                                    return true
                                                }
                                            }
                                            beforeAgent true
                                            beforeOptions true
                                        }
                                        steps{
                                            script{
                                                milestone 1
                                                withSonarQubeEnv(installationName:'sonarcloud', credentialsId: params.SONARCLOUD_TOKEN) {
                                                    def sourceInstruction
                                                    if (env.CHANGE_ID){
                                                        sourceInstruction = '-Dsonar.pullrequest.key=$CHANGE_ID -Dsonar.pullrequest.base=$BRANCH_NAME'
                                                    } else{
                                                        sourceInstruction = '-Dsonar.branch.name=$BRANCH_NAME'
                                                    }
                                                    withCredentials([string(credentialsId: params.SONARCLOUD_TOKEN, variable: 'token')]) {
                                                        sh(
                                                            label: 'Running Sonar Scanner',
                                                            script: "uv run pysonar -t \$token -Dsonar.projectVersion=$VERSION -Dsonar.buildString=\"$BUILD_TAG\" ${sourceInstruction}"
                                                        )
                                                    }
                                                }
                                                timeout(time: 1, unit: 'HOURS') {
                                                    def sonarqube_result = waitForQualityGate(abortPipeline: false)
                                                    if (sonarqube_result.status != 'OK') {
                                                        unstable "SonarQube quality gate: ${sonarqube_result.status}"
                                                    }
                                                    if(env.BRANCH_IS_PRIMARY){
                                                        writeJSON file: 'reports/sonar-report.json', json: get_sonarqube_unresolved_issues('.sonar/report-task.txt')
                                                        recordIssues(tools: [sonarQube(pattern: 'reports/sonar-report.json')])
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                                post{
                                    cleanup{
                                        sh 'git clean -dfx'
                                    }
                                }
                            }
                        }
                    }
                    stage('Tox'){
                        when{
                            equals expected: true, actual: params.TEST_RUN_TOX
                        }
                        parallel{
                            stage('Linux'){
                                when{
                                    expression {return nodesByLabel('linux && docker && x86').size() > 0}
                                }
                                environment{
                                     PIP_CACHE_DIR='/tmp/pipcache'
                                     UV_TOOL_DIR='/tmp/uvtools'
                                     UV_PYTHON_CACHE_DIR='/tmp/uvpython'
                                     UV_CACHE_DIR='/tmp/uvcache'
                                }
                                steps{
                                    script{
                                        def envs = []
                                        node('docker && linux'){
                                            checkout scm
                                            withEnv(["UV_CONFIG_FILE=${createUnixUvConfig()}"]){
                                                try{
                                                    docker.image('ghcr.io/astral-sh/uv:debian').inside('--mount source=python-tmp-hathivalidate,target=/tmp --tmpfs /ci_tmp:exec -e TOX_WORK_DIR=/ci_tmp/tox -e UV_PROJECT_ENVIRONMENT=/ci_tmp/venv'){
                                                        envs = sh(
                                                            label: 'Get tox environments',
                                                            script: 'uv run --isolated --only-group=tox --frozen --quiet tox list -d --no-desc',
                                                            returnStdout: true,
                                                        ).trim().split('\n')
                                                    }
                                                } finally{
                                                    sh "${tool(name: 'Default', type: 'git')} clean -dfx"
                                                }
                                            }
                                        }
                                        parallel(
                                            envs.collectEntries{toxEnv ->
                                                def version = toxEnv.replaceAll(/py(\d)(\d+)/, '$1.$2')
                                                [
                                                    "Tox Environment: ${toxEnv}",
                                                    {
                                                        node('docker && linux'){
                                                            checkout scm
                                                            withEnv(["UV_CONFIG_FILE=${createUnixUvConfig()}"]){
                                                                try{
                                                                    docker.image('ghcr.io/astral-sh/uv:debian').inside('--mount source=python-tmp-hathivalidate,target=/tmp --tmpfs /.local/share:exec --tmpfs /.local/bin:exec --tmpfs /ci_tmp:exec -e TOX_WORK_DIR=/ci_tmp/tox -e UV_PROJECT_ENVIRONMENT=/ci_tmp/venv'){
                                                                        retry(3){
                                                                            try{
                                                                                sh( label: 'Running Tox',
                                                                                    script: """uv python install cpython-${version}
                                                                                               uv run -p ${version} --frozen --only-group=tox-uv tox run --runner uv-venv-lock-runner -e ${toxEnv}
                                                                                            """
                                                                                    )
                                                                            } catch(e) {
                                                                                cleanWs(
                                                                                    patterns: [
                                                                                        [pattern: '.tox', type: 'INCLUDE'],
                                                                                    ]
                                                                                )
                                                                                throw e
                                                                            }
                                                                        }
                                                                    }
                                                                } finally{
                                                                    sh "${tool(name: 'Default', type: 'git')} clean -dfx"
                                                                }
                                                            }
                                                        }
                                                    }
                                                ]
                                            }
                                        )
                                    }
                                }
                            }
                            stage('Windows'){
                                when{
                                    expression {return nodesByLabel('windows && docker && x86').size() > 0}
                                }
                                environment{
                                     PIP_CACHE_DIR='C:\\Users\\ContainerUser\\Documents\\cache\\pipcache'
                                     UV_TOOL_DIR='C:\\Users\\ContainerUser\\Documents\\uvtools'
                                     UV_PYTHON_CACHE_DIR='C:\\Users\\ContainerUser\\Documents\\cache\\uvpython'
                                     UV_CACHE_DIR='C:\\Users\\ContainerUser\\Documents\\cache\\uvcache'
                                }
                                steps{
                                    script{
                                        def envs = []
                                        node('docker && windows'){
                                            checkout scm
                                            withEnv(["UV_CONFIG_FILE=${createWindowUVConfig()}",]){
                                                try{
                                                    docker.image(env.DEFAULT_PYTHON_DOCKER_IMAGE ? env.DEFAULT_PYTHON_DOCKER_IMAGE: 'python')
                                                        .inside(
                                                            "--mount type=volume,source=uv_python_cache_dir,target=${env.UV_PYTHON_CACHE_DIR}"
                                                         + " --mount type=volume,source=pipcache,target=${env.PIP_CACHE_DIR}"
                                                         + " --mount type=volume,source=uv_cache_dir,target=${env.UV_CACHE_DIR}"
                                                        ){
                                                        bat(script: 'python -m venv venv && venv\\Scripts\\pip install --disable-pip-version-check uv')
                                                        envs = bat(
                                                            label: 'Get tox environments',
                                                            script: '@.\\venv\\Scripts\\uv run --isolated --only-group tox --frozen --quiet tox list -d --no-desc',
                                                            returnStdout: true,
                                                        ).trim().split('\r\n')
                                                    }
                                                } finally{
                                                    bat "${tool(name: 'Default', type: 'git')} clean -dfx"
                                                }
                                            }
                                        }
                                        parallel(
                                            envs.collectEntries{toxEnv ->
                                                def version = toxEnv.replaceAll(/py(\d)(\d+)/, '$1.$2')
                                                [
                                                    "Tox Environment: ${toxEnv}",
                                                    {
                                                        node('docker && windows'){
                                                            checkout scm
                                                            withEnv(["UV_CONFIG_FILE=${createWindowUVConfig()}", "TOX_UV_PATH=${WORKSPACE}\\venv\\Scripts\\uv.exe"]){
                                                                try{
                                                                    docker.image(env.DEFAULT_PYTHON_DOCKER_IMAGE ? env.DEFAULT_PYTHON_DOCKER_IMAGE: 'python')
                                                                        .inside(
                                                                            "--mount type=volume,source=uv_python_cache_dir,target=${env.UV_PYTHON_CACHE_DIR}"
                                                                         + " --mount type=volume,source=pipcache,target=${env.PIP_CACHE_DIR}"
                                                                         + " --mount type=volume,source=uv_cache_dir,target=${env.UV_CACHE_DIR}"
                                                                        ){
                                                                        bat(label: 'Install uv',
                                                                            script: 'python -m venv venv && venv\\Scripts\\pip install --disable-pip-version-check uv'
                                                                        )
                                                                        retry(3){
                                                                            try{
                                                                                bat(label: 'Running Tox',
                                                                                    script: """venv\\Scripts\\uv python install cpython-${version}
                                                                                               venv\\Scripts\\uv run -p ${version} --frozen --only-group=tox-uv tox run --runner uv-venv-lock-runner -e ${toxEnv}
                                                                                            """
                                                                                )
                                                                            } catch(e){
                                                                                cleanWs(
                                                                                    patterns: [
                                                                                        [pattern: '.tox', type: 'INCLUDE'],
                                                                                    ]
                                                                                )
                                                                                throw e
                                                                            }
                                                                        }
                                                                    }
                                                                } finally{
                                                                    bat "${tool(name: 'Default', type: 'git')} clean -dfx"
                                                                }
                                                            }
                                                        }
                                                    }
                                                ]
                                            }
                                        )
                                    }
                                }
                            }
                        }
                    }
                }
            }
            stage('Packaging') {
                when{
                    anyOf{
                        equals expected: true, actual: params.BUILD_PACKAGES
                    }
                    beforeAgent true
                }
                stages{
                    stage('Building Source and Wheel formats'){
                        agent {
                            docker{
                                image 'ghcr.io/astral-sh/uv:debian'
                                label 'linux && docker'
                                args '--mount source=python-tmp-hathivalidate,target=/tmp'
                              }
                        }
                        environment{
                            PIP_CACHE_DIR='/tmp/pipcache'
                            UV_CACHE_DIR='/tmp/uvcache'
                            UV_FROZEN='1'
                            UV_CONFIG_FILE=createUnixUvConfig()
                        }
                        options {
                            retry(2)
                        }
                        steps{
                            timeout(5){
                                sh(
                                    label: 'Package',
                                    script: 'uv build'
                                )
                            }
                            stash includes: 'dist/*.whl,dist/*.tar.gz,dist/*.zip', name: 'PYTHON_PACKAGES'
                            archiveArtifacts artifacts: 'dist/*.whl,dist/*.tar.gz,dist/*.zip', fingerprint: true
                        }
                        post{
                            cleanup{
                                cleanWs(
                                    deleteDirs: true,
                                    patterns: [
                                        [pattern: 'uv.toml', type: 'INCLUDE'],
                                        [pattern: '**/*.egg-info/', type: 'INCLUDE'],
                                        [pattern: '**/*.dist-info/', type: 'INCLUDE'],
                                        [pattern: '**/__pycache__/', type: 'INCLUDE'],
                                        [pattern: 'venv/', type: 'INCLUDE'],
                                        [pattern: 'dist/', type: 'INCLUDE']
                                    ]
                                )
                            }
                        }
                    }
                    stage('Testing Packages'){
                        when{
                            equals expected: true, actual: params.TEST_PACKAGES
                        }
                        steps{
                            customMatrix(
                                axes: [
                                    [
                                        name: 'PYTHON_VERSION',
                                        values: ['3.10', '3.11', '3.12', '3.13', '3.14', '3.14t']
                                    ],
                                    [
                                        name: 'OS',
                                        values: ['linux','macos','windows']
                                    ],
                                    [
                                        name: 'ARCHITECTURE',
                                        values: ['x86_64', 'arm64']
                                    ],
                                    [
                                        name: 'PACKAGE_TYPE',
                                        values: ['wheel', 'sdist'],
                                    ]
                                ],
                                excludes: [
                                    [
                                        [
                                            name: 'OS',
                                            values: 'windows'
                                        ],
                                        [
                                            name: 'ARCHITECTURE',
                                            values: 'arm64',
                                        ]
                                    ]
                                ],
                                when: {entry -> "INCLUDE_${entry.OS}-${entry.ARCHITECTURE}".toUpperCase() && params["INCLUDE_${entry.OS}-${entry.ARCHITECTURE}".toUpperCase()]},
                                stages: [
                                    { entry ->
                                        stage('Test Package') {
                                            retry(3){
                                                node("${entry.OS} && ${entry.ARCHITECTURE} ${['linux', 'windows'].contains(entry.OS) ? '&& docker': ''}"){
                                                    try{
                                                        checkout scm
                                                        unstash 'PYTHON_PACKAGES'
                                                        if(['linux', 'windows'].contains(entry.OS) && params.containsKey("INCLUDE_${entry.OS}-${entry.ARCHITECTURE}".toUpperCase()) && params["INCLUDE_${entry.OS}-${entry.ARCHITECTURE}".toUpperCase()]){
                                                            docker.image(isUnix() ? 'ghcr.io/astral-sh/uv:debian': 'python')
                                                                .inside(
                                                                    isUnix() ?
                                                                        '--mount source=python-tmp-hathivalidate,target=/tmp '
                                                                        + '--tmpfs /.local/share:exec --tmpfs /.local/bin:exec '
                                                                        + '--tmpfs /ci_tmp:exec -e TOX_WORK_DIR=/ci_tmp/tox -e UV_PROJECT_ENVIRONMENT=/ci_tmp/venv'
                                                                    :
                                                                        '--mount type=volume,source=uv_python_cache_dir,target=C:\\Users\\ContainerUser\\Documents\\cache\\uvpython'
                                                                        + ' --mount type=volume,source=pipcache,target=C:\\Users\\ContainerUser\\Documents\\cache\\pipcache'
                                                                        + ' --mount type=volume,source=uv_cache_dir,target=C:\\Users\\ContainerUser\\Documents\\cache\\uvcache'
                                                                ){
                                                                 if(isUnix()){
                                                                    withEnv([
                                                                        'PIP_CACHE_DIR=/tmp/pipcache',
                                                                        'UV_TOOL_DIR=/tmp/uvtools',
                                                                        'UV_PYTHON_CACHE_DIR=/tmp/uvpython',
                                                                        'UV_CACHE_DIR=/tmp/uvcache',
                                                                        "UV_CONFIG_FILE=${createUnixUvConfig()}",
                                                                    ]){
                                                                         sh(
                                                                            label: 'Testing with tox',
                                                                            script: """uv python install cpython-${entry.PYTHON_VERSION}
                                                                                       uv run -p ${entry.PYTHON_VERSION} --frozen --only-group=tox-uv tox --installpkg ${findFiles(glob: entry.PACKAGE_TYPE == 'wheel' ? 'dist/*.whl' : 'dist/*.tar.gz')[0].path} -e py${entry.PYTHON_VERSION.replace('.', '')}
                                                                                    """
                                                                        )
                                                                    }
                                                                 } else {
                                                                    withEnv([
                                                                        'PIP_CACHE_DIR=C:\\Users\\ContainerUser\\Documents\\cache\\pipcache',
                                                                        'UV_TOOL_DIR=C:\\Users\\ContainerUser\\Documents\\uvtools',
                                                                        'UV_PYTHON_CACHE_DIR=C:\\Users\\ContainerUser\\Documents\\cache\\uvpython',
                                                                        'UV_CACHE_DIR=C:\\Users\\ContainerUser\\Documents\\cache\\uvcache',
                                                                        "UV_CONFIG_FILE=${createWindowUVConfig()}",
                                                                        "TOX_UV_PATH=${WORKSPACE}\\venv\\Scripts\\uv.exe"
                                                                    ]){
                                                                        bat(
                                                                            label: 'Testing with tox',
                                                                            script: """python -m venv venv
                                                                                       .\\venv\\Scripts\\pip install --disable-pip-version-check uv
                                                                                       .\\venv\\Scripts\\uv python install cpython-${entry.PYTHON_VERSION}
                                                                                       .\\venv\\Scripts\\uv run -p ${entry.PYTHON_VERSION} --frozen --only-group=tox-uv tox --installpkg ${findFiles(glob: entry.PACKAGE_TYPE == 'wheel' ? 'dist/*.whl' : 'dist/*.tar.gz')[0].path} -e py${entry.PYTHON_VERSION.replace('.', '')}
                                                                                    """
                                                                        )
                                                                    }
                                                                 }
                                                            }
                                                        } else {
                                                            if(isUnix()){
                                                                withEnv([
                                                                    "UV_CONFIG_FILE=${createUnixUvConfig()}",
                                                                    "TOX_UV_PATH=${WORKSPACE}/venv/bin/uv"
                                                                ]){
                                                                    sh(
                                                                        label: 'Testing with tox',
                                                                        script: """python3 -m venv venv
                                                                                   ./venv/bin/pip install --disable-pip-version-check uv
                                                                                   ./venv/bin/uv run -p ${entry.PYTHON_VERSION} --frozen --only-group=tox-uv tox --installpkg ${findFiles(glob: entry.PACKAGE_TYPE == 'wheel' ? 'dist/*.whl' : 'dist/*.tar.gz')[0].path} -e py${entry.PYTHON_VERSION.replace('.', '')}
                                                                                """
                                                                    )
                                                                }
                                                            } else {
                                                                withEnv(["UV_CONFIG_FILE=${createWindowUVConfig()}"]){
                                                                    bat(
                                                                        label: 'Testing with tox',
                                                                        script: """python -m venv venv
                                                                                   .\\venv\\Scripts\\pip install --disable-pip-version-check uv
                                                                                   .\\venv\\Scripts\\uv python install cpython-${entry.PYTHON_VERSION}
                                                                                   .\\venv\\Scripts\\uv run -p ${entry.PYTHON_VERSION} --frozen --only-group=tox-uv tox --installpkg ${findFiles(glob: entry.PACKAGE_TYPE == 'wheel' ? 'dist/*.whl' : 'dist/*.tar.gz')[0].path} -e py${entry.PYTHON_VERSION.replace('.', '')}
                                                                                """
                                                                    )
                                                                }
                                                            }
                                                        }
                                                    } finally{
                                                        if(isUnix()){
                                                            sh "${tool(name: 'Default', type: 'git')} clean -dfx"
                                                        } else {
                                                            bat "${tool(name: 'Default', type: 'git')} clean -dfx"
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                ]
                            )
                        }
                    }
                }
            }
            stage('Deploy'){
                parallel {
                    stage('Deploy to pypi') {
                        environment{
                            PIP_CACHE_DIR='/tmp/pipcache'
                            UV_TOOL_DIR='/tmp/uvtools'
                            UV_PYTHON_CACHE_DIR='/tmp/uvpython'
                            UV_CACHE_DIR='/tmp/uvcache'
                        }
                        agent {
                            docker{
                                image 'ghcr.io/astral-sh/uv:debian'
                                label 'docker && linux'
                                args '--mount source=python-tmp-hathivalidate,target=/tmp'
                            }
                        }
                        when{
                            allOf{
                                equals expected: true, actual: params.DEPLOY_PYPI
                                equals expected: true, actual: params.BUILD_PACKAGES

                            }
                            beforeAgent true
                            beforeInput true
                        }
                        options{
                            retry(3)
                        }
                        input {
                            message 'Upload to pypi server?'
                            parameters {
                                choice(
                                    choices: getPypiConfig(),
                                    description: 'Url to the pypi index to upload python packages.',
                                    name: 'SERVER_URL'
                                )
                            }
                        }
                        steps{
                            unstash 'PYTHON_PACKAGES'
                            withEnv(["UV_PUBLISH_URL=${SERVER_URL}"]){
                                withCredentials([
                                    usernamePassword(
                                        credentialsId: 'jenkins-nexus',
                                        passwordVariable: 'UV_PUBLISH_PASSWORD',
                                        usernameVariable: 'UV_PUBLISH_USERNAME'
                                    )
                                ]){
                                    sh(
                                        label: 'Uploading to pypi',
                                        script: 'uv publish dist/*'
                                    )
                                }
                            }
                        }
                        post{
                            cleanup{
                                cleanWs(
                                    deleteDirs: true,
                                    patterns: [
                                            [pattern: 'dist/', type: 'INCLUDE']
                                        ]
                                )
                            }
                        }
                    }
                    stage('Deploy Online Documentation') {
                        when{
                            equals expected: true, actual: params.DEPLOY_DOCS
                            beforeAgent true
                            beforeInput true
                        }
                        environment{
                            PIP_CACHE_DIR='/tmp/pipcache'
                            UV_TOOL_DIR='/tmp/uvtools'
                            UV_PYTHON_CACHE_DIR='/tmp/uvpython'
                            UV_CACHE_DIR='/tmp/uvcache'
                        }
                        agent {
                            docker{
                                image 'python'
                                label 'docker && linux'
                                args '--mount source=python-tmp-hathivalidate,target=/tmp'
                            }
                        }
                        options{
                            timeout(time: 1, unit: 'DAYS')
                        }
                        input {
                            message 'Update project documentation?'
                        }
                        steps{
                            unstash 'DOCUMENTATION'
                            withCredentials([usernamePassword(credentialsId: 'dccdocs-server', passwordVariable: 'docsPassword', usernameVariable: 'docsUsername')]) {
                                sh 'python utils/upload_docs.py --username=$docsUsername --password=$docsPassword --subroute=hathi_validate build/docs/html apache-ns.library.illinois.edu'
                            }
                        }
                        post{
                            cleanup{
                                cleanWs(
                                        deleteDirs: true,
                                        patterns: [
                                            [pattern: 'build/', type: 'INCLUDE'],
                                            [pattern: 'dist/', type: 'INCLUDE'],
                                            ]
                                    )
                            }
                        }
                    }
                }
            }
        }
    }
}