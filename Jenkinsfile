library identifier: 'JenkinsPythonHelperLibrary@2024.1.2', retriever: modernSCM(
  [$class: 'GitSCMSource',
   remote: 'https://github.com/UIUCLibrary/JenkinsPythonHelperLibrary.git',
   ])


// ****************************************************************************
//  Constants
//
// ============================================================================
// Versions of python that are supported
// ----------------------------------------------------------------------------
SUPPORTED_MAC_VERSIONS = ['3.8', '3.9', '3.10', '3.11', '3.12']
SUPPORTED_LINUX_VERSIONS = ['3.8', '3.9', '3.10', '3.11', '3.12']
SUPPORTED_WINDOWS_VERSIONS = ['3.8', '3.9', '3.10', '3.11', '3.12']

// ============================================================================

defaultParameterValues = [
    USE_SONARQUBE: false
]


def getPypiConfig() {
    node(){
        configFileProvider([configFile(fileId: 'pypi_config', variable: 'CONFIG_FILE')]) {
            def config = readJSON( file: CONFIG_FILE)
            return config['deployment']['indexes']
        }
    }
}

def startup(){
    parallel(
        [
            failFast: true,
            'Getting Distribution Info': {
                node('linux && docker') {
                    timeout(2){
                        ws{
                            checkout scm
                            try{
                                docker.image('python').inside {
                                    withEnv(['PIP_NO_CACHE_DIR=off']) {
                                        sh(
                                           label: 'Running setup.py with dist_info',
                                           script: '''python --version
                                                      python setup.py dist_info
                                                   '''
                                        )
                                    }
                                    stash includes: '*.dist-info/**', name: 'DIST-INFO'
                                    archiveArtifacts artifacts: '*.dist-info/**'
                                }
                            } finally{
                                deleteDir()
                            }
                        }
                    }
                }
            }
        ]
    )
}
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
        booleanParam(name: 'INCLUDE_LINUX_ARM', defaultValue: false, description: 'Include ARM architecture for Linux')
        booleanParam(name: 'INCLUDE_LINUX_X86_64', defaultValue: true, description: 'Include x86_64 architecture for Linux')
        booleanParam(name: 'INCLUDE_MACOS_ARM', defaultValue: false, description: 'Include ARM(m1) architecture for Mac')
        booleanParam(name: 'INCLUDE_MACOS_X86_64', defaultValue: false, description: 'Include x86_64 architecture for Mac')
        booleanParam(name: 'INCLUDE_WINDOWS_X86_64', defaultValue: true, description: 'Include x86_64 architecture for Windows')
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
                        dockerfile {
                            filename 'ci/docker/python/linux/jenkins/Dockerfile'
                            label 'linux && docker && x86'
                        }
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
                            sh(script: '''mkdir -p logs
                                          python -m sphinx -b html docs/source build/docs/html -d build/docs/doctrees -w logs/build_sphinx.log -W --keep-going
                                       '''
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
                            cleanWs notFailBuild: true
                        }
                    }
                }
                stage('Checks') {
                    when{
                        equals expected: true, actual: params.RUN_CHECKS
                    }
                    stages{
                        stage('Code Quality'){
                            agent {
                                dockerfile {
                                    filename 'ci/docker/python/linux/jenkins/Dockerfile'
                                    label 'linux && docker && x86'
                                    args '--mount source=sonar-cache-hathi_validate,target=/opt/sonar/.sonar/cache'
                                }
                            }
                            options {
                              retry(conditions: [agent()], count: 3)
                            }
                            stages{
                                stage('Set up Tests') {
                                    steps{
                                        sh(label: 'Adding logs and reports directories',
                                           script: '''
                                                mkdir -p logs
                                                mkdir -p reports
                                                '''
                                           )
                                    }
                                }
                                stage('Running Tests') {
                                    parallel {
                                        stage('PyTest'){
                                            steps{
                                                sh(
                                                    label: 'Running pytest',
                                                    script: 'coverage run --parallel-mode --source=hathi_validate -m pytest --junitxml=./reports/pytest-junit.xml -p no:cacheprovider'
                                                )

                                            }
                                            post {
                                                always{
                                                    junit 'reports/pytest-junit.xml'
                                                    stash includes: 'reports/pytest-junit.xml', name: 'PYTEST_UNIT_TEST_RESULTS'
                                                }
                                            }
                                        }
                                        stage('MyPy'){
                                            steps{
                                                catchError(buildResult: 'SUCCESS', message: 'MyPy found issues', stageResult: 'UNSTABLE') {
                                                    sh(label: 'Running MyPy',
                                                       script: '''mypy -p hathi_validate --html-report reports/mypy_html --cache-dir=/dev/null > logs/mypy.log'''
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
                                                       script: 'flake8 hathi_validate --tee --output-file=logs/flake8.log'
                                                    )
                                                }
                                            }
                                            post {
                                                always {
                                                    stash includes: 'logs/flake8.log', name: 'FLAKE8_REPORT'
                                                    recordIssues(tools: [flake8(name: 'Flake8', pattern: 'logs/flake8.log')])
                                                }
                                            }
                                        }
                                        stage('Task Scanner'){
                                            steps{
                                                recordIssues(tools: [taskScanner(highTags: 'FIXME', includePattern: 'hathi_validate/**/*.py', normalTags: 'TODO')])
                                            }
                                        }
                                        stage('Behave') {
                                            steps {
                                                catchError(buildResult: 'UNSTABLE', message: 'Did not pass all Behave BDD tests', stageResult: 'UNSTABLE') {
                                                    sh(
                                                        script: 'coverage run --parallel-mode --source=hathi_validate -m behave --junit --junit-directory reports/tests/behave'
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
                                                            script: '''mkdir -p reports
                                                                       pydocstyle hathi_validate
                                                                       '''
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
                                                            script: 'pylint hathi_validate -r n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" --persistent=no'
                                                        )
                                                    }
                                                }
                                                sh(
                                                    script: 'pylint hathi_validate -r n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" --persistent=no > reports/pylint_issues.txt',
                                                    label: 'Running pylint for sonarqube',
                                                    returnStatus: true
                                                )
                                            }
                                            post{
                                                always{
                                                    recordIssues(tools: [pyLint(pattern: 'reports/pylint.txt')])
                                                    stash includes: 'reports/pylint_issues.txt,reports/pylint.txt', name: 'PYLINT_REPORT'
                                                }
                                            }
                                        }
                                        stage('Doctest'){
                                            steps{
                                                sh "python -m sphinx -b doctest docs/source build/docs -d build/docs/doctrees -v"
                                            }

                                        }
                                    }
                                    post{
                                        always{
                                            sh(label: 'Combining Coverage Data',
                                               script: '''coverage combine
                                                          coverage xml -o ./reports/coverage.xml
                                                          '''
                                            )
                                            stash(includes: 'reports/coverage*.xml', name: 'COVERAGE_REPORT_DATA')
                                            recordCoverage(tools: [[parser: 'COBERTURA', pattern: 'reports/coverage.xml']])
                                        }
                                    }
                                }
                                stage('Run Sonarqube Analysis'){
                                    options{
                                        lock('hathivalidate-sonarscanner')
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
                                            def sonarqube = load('ci/jenkins/scripts/sonarqube.groovy')
                                            def props = readTOML( file: 'pyproject.toml')['project']
                                            def stashes = [
                                                'COVERAGE_REPORT_DATA',
                                                'PYTEST_UNIT_TEST_RESULTS',
                                                'PYLINT_REPORT',
                                                'FLAKE8_REPORT'
                                            ]
                                            def sonarqubeConfig = [
                                                installationName: 'sonarcloud',
                                                credentialsId: params.SONARCLOUD_TOKEN,
                                            ]
                                            if (env.CHANGE_ID){
                                                sonarqube.submitToSonarcloud(
                                                    reportStashes: stashes,
                                                    artifactStash: 'sonarqube artifacts',
                                                    sonarqube: sonarqubeConfig,
                                                    pullRequest: [
                                                        source: env.CHANGE_ID,
                                                        destination: env.BRANCH_NAME,
                                                    ],
                                                    package: [
                                                        version: props.version,
                                                        name: props.name
                                                    ],
                                                )
                                            } else {
                                                sonarqube.submitToSonarcloud(
                                                    reportStashes: stashes,
                                                    artifactStash: 'sonarqube artifacts',
                                                    sonarqube: sonarqubeConfig,
                                                    package: [
                                                        version: props.version,
                                                        name: props.name
                                                    ]
                                                )
                                            }
                                        }
                                    }
                                    post {
                                        always{
                                            node(''){
                                                unstash 'sonarqube artifacts'
                                                recordIssues(tools: [sonarQube(pattern: 'reports/sonar-report.json')])
                                            }
                                        }
                                    }
                                }
                            }
                            post{
                                cleanup{
                                    cleanWs(
                                        deleteDirs: true,
                                        patterns: [
                                            [pattern: 'logs/', type: 'INCLUDE'],
                                            [pattern: 'reports/', type: 'INCLUDE'],
                                            [pattern: '.coverage.*/', type: 'INCLUDE'],
                                            [pattern: '**/__pycache__/', type: 'INCLUDE'],
                                        ]
                                    )
                                }
                            }
                        }
                    }
                }
                stage('Tox'){
                    when{
                        equals expected: true, actual: params.TEST_RUN_TOX
                    }
                    options{
                        lock("hathivalidate-${env.BRANCH_NAME}-tox")
                    }
                    parallel{
                        stage('Linux'){
                            when{
                                expression {return nodesByLabel('linux && docker && x86').size() > 0}
                            }
                            steps{
                                script{
                                    parallel(
                                        getToxTestsParallel(
                                            envNamePrefix: 'Tox Linux',
                                            label: 'linux && docker && x86',
                                            dockerfile: 'ci/docker/python/linux/tox/Dockerfile',
                                            dockerArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg PIP_DOWNLOAD_CACHE=/.cache/pip',
                                            dockerRunArgs: '-v pipcache_hathivalidate:/.cache/pip',
                                            retry: 2
                                        )
                                    )
                                }
                            }
                        }
                        stage('Windows'){
                            when{
                                expression {return nodesByLabel('windows && docker && x86').size() > 0}
                            }
                            steps{
                                script{
                                    parallel(
                                         getToxTestsParallel(
                                            envNamePrefix: 'Tox Windows',
                                            label: 'windows && docker && x86',
                                            dockerfile: 'ci/docker/python/windows/tox/Dockerfile',
                                            dockerArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg CHOCOLATEY_SOURCE --build-arg PIP_DOWNLOAD_CACHE=c:/users/containeradministrator/appdata/local/pip',
                                            dockerRunArgs: '-v pipcache_hathivalidate:c:/users/containeradministrator/appdata/local/pip',
                                            retry: 2
                                        )
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
                            image 'python'
                            label 'linux && docker'
                          }
                    }
                    options {
                      retry(3)
                    }
                    steps{
                        timeout(5){
                            withEnv(['PIP_NO_CACHE_DIR=off']) {
                                sh(label: 'Build Python Package',
                                   script: '''python -m venv venv --upgrade-deps
                                              venv/bin/pip install build
                                              venv/bin/python -m build .
                                              '''
                                    )
                            }
                        }
                    }
                    post{
                        success{
                            archiveArtifacts artifacts: 'dist/*.whl,dist/*.tar.gz,dist/*.zip', fingerprint: true
                        }
                        always{
                            stash includes: 'dist/*.whl', name: 'wheel'
                            stash includes: 'dist/*.zip,dist/*.tar.gz', name: 'sdist'
                        }
                        cleanup{
                            cleanWs(
                                deleteDirs: true,
                                patterns: [
                                    [pattern: '**/__pycache__/', type: 'INCLUDE'],
                                    [pattern: 'venv/', type: 'INCLUDE'],
                                    [pattern: 'dist/', type: 'INCLUDE']
                                ]
                            )
                        }
                    }
                }
                stage('Testing Python Packages'){
                    when{
                        equals expected: true, actual: params.TEST_PACKAGES
                        beforeAgent true
                    }
                    steps{
                        script{
                            def windowsTests = [:]
                            if(params.INCLUDE_WINDOWS_X86_64 == true){
                                SUPPORTED_WINDOWS_VERSIONS.each{ pythonVersion ->
                                    windowsTests["Windows - Python ${pythonVersion}: sdist"] = {
                                        testPythonPkg(
                                            agent: [
                                                dockerfile: [
                                                    label: 'windows && docker && x86',
                                                    filename: 'ci/docker/python/windows/tox/Dockerfile',
                                                    additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg CHOCOLATEY_SOURCE --build-arg PIP_DOWNLOAD_CACHE=c:/users/containeradministrator/appdata/local/pip',
                                                    args: '-v pipcache_hathivalidate:c:/users/containeradministrator/appdata/local/pip'
                                                ]
                                            ],
                                            retries: 3,
                                            testSetup: {
                                                checkout scm
                                                unstash 'sdist'
                                            },
                                            testCommand: {
                                                findFiles(glob: 'dist/*.tar.gz').each{
                                                    bat(label: 'Running Tox', script: "tox --workdir %TEMP%\\tox --installpkg ${it.path} -e py${pythonVersion.replace('.', '')} -v")
                                                }
                                            },
                                            post:[
                                                cleanup: {
                                                    cleanWs(
                                                        patterns: [
                                                            [pattern: 'dist/', type: 'INCLUDE'],
                                                            [pattern: '**/__pycache__/', type: 'INCLUDE'],
                                                        ],
                                                        notFailBuild: true,
                                                        deleteDirs: true
                                                    )
                                                },
                                            ]
                                        )
                                    }
                                    windowsTests["Windows - Python ${pythonVersion}: wheel"] = {
                                        testPythonPkg(
                                            agent: [
                                                dockerfile: [
                                                    label: 'windows && docker && x86',
                                                    filename: 'ci/docker/python/windows/tox/Dockerfile',
                                                    additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg CHOCOLATEY_SOURCE --build-arg PIP_DOWNLOAD_CACHE=c:/users/containeradministrator/appdata/local/pip',
                                                    args: '-v pipcache_hathivalidate:c:/users/containeradministrator/appdata/local/pip'
                                                ]
                                            ],
                                            retries: 3,
                                            testSetup: {
                                                 checkout scm
                                                 unstash 'wheel'
                                            },
                                            testCommand: {
                                                 findFiles(glob: 'dist/*.whl').each{
                                                     powershell(label: 'Running Tox', script: "tox --installpkg ${it.path} --workdir \$env:TEMP\\tox  -e py${pythonVersion.replace('.', '')}")
                                                 }

                                            },
                                            post:[
                                                cleanup: {
                                                    cleanWs(
                                                        patterns: [
                                                                [pattern: 'dist/', type: 'INCLUDE'],
                                                                [pattern: '**/__pycache__/', type: 'INCLUDE'],
                                                            ],
                                                        notFailBuild: true,
                                                        deleteDirs: true
                                                    )
                                                },
                                                success: {
                                                    archiveArtifacts artifacts: 'dist/*.whl'
                                                }
                                            ]
                                        )
                                    }
                                }
                            }
                            def linuxTests = [:]
                            def linuxArchitectures = []
                            if(params.INCLUDE_LINUX_X86_64 == true){
                                linuxArchitectures.add('x86_64')
                            }
                            if(params.INCLUDE_LINUX_ARM == true){
                                linuxArchitectures.add('arm64')
                            }
                            SUPPORTED_LINUX_VERSIONS.each{ pythonVersion ->
                                linuxArchitectures.each{arch ->
                                    linuxTests["Linux ${arch} - Python ${pythonVersion}: sdist"] = {
                                        testPythonPkg(
                                            agent: [
                                                dockerfile: [
                                                    label: "linux && docker && ${arch}",
                                                    filename: 'ci/docker/python/linux/tox/Dockerfile',
                                                    additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg PIP_DOWNLOAD_CACHE=/.cache/pip',
                                                    args: '-v pipcache_hathivalidate:/.cache/pip',
                                                ]
                                            ],
                                            retries: 3,
                                            testSetup: {
                                                checkout scm
                                                unstash 'sdist'
                                            },
                                            testCommand: {
                                                findFiles(glob: 'dist/*.tar.gz').each{
                                                    sh(
                                                        label: 'Running Tox',
                                                        script: "tox --installpkg ${it.path} --workdir /tmp/tox -e py${pythonVersion.replace('.', '')}"
                                                        )
                                                }
                                            },
                                            post:[
                                                cleanup: {
                                                    cleanWs(
                                                        patterns: [
                                                                [pattern: 'dist/', type: 'INCLUDE'],
                                                                [pattern: '**/__pycache__/', type: 'INCLUDE'],
                                                            ],
                                                        notFailBuild: true,
                                                        deleteDirs: true
                                                    )
                                                },
                                            ]
                                        )
                                    }
                                    linuxTests["Linux ${arch} - Python ${pythonVersion}: wheel"] = {
                                        testPythonPkg(
                                            agent: [
                                                dockerfile: [
                                                    label: "linux && docker && ${arch}",
                                                    filename: 'ci/docker/python/linux/tox/Dockerfile',
                                                    additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg PIP_DOWNLOAD_CACHE=/.cache/pip',
                                                    args: '-v pipcache_hathivalidate:/.cache/pip',
                                                ]
                                            ],
                                            testSetup: {
                                                checkout scm
                                                unstash 'wheel'
                                            },
                                            testCommand: {
                                                findFiles(glob: 'dist/*.whl').each{
                                                    timeout(5){
                                                        sh(
                                                            label: 'Running Tox',
                                                            script: "tox --installpkg ${it.path} --workdir /tmp/tox -e py${pythonVersion.replace('.', '')}"
                                                            )
                                                    }
                                                }
                                            },
                                            post:[
                                                cleanup: {
                                                    cleanWs(
                                                        patterns: [
                                                                [pattern: 'dist/', type: 'INCLUDE'],
                                                                [pattern: '**/__pycache__/', type: 'INCLUDE'],
                                                            ],
                                                        notFailBuild: true,
                                                        deleteDirs: true
                                                    )
                                                },
                                                success: {
                                                    archiveArtifacts artifacts: 'dist/*.whl'
                                                },
                                            ]
                                        )
                                    }
                                }
                            }
                            def macTests = [:]
                            SUPPORTED_MAC_VERSIONS.each{ pythonVersion ->
                                def macArchitectures = []
                                if(params.INCLUDE_MACOS_X86_64 == true){
                                    macArchitectures.add('x86_64')
                                }
                                if(params.INCLUDE_MACOS_ARM == true){
                                    macArchitectures.add('arm64')
                                }
                                macArchitectures.each{ processorArchitecture ->
                                    if (nodesByLabel("mac && ${processorArchitecture} && python${pythonVersion}").size() > 0){
                                        macTests["Mac ${processorArchitecture} - Python ${pythonVersion}: sdist"] = {
                                            testPythonPkg(
                                                agent: [
                                                    label: "mac && python${pythonVersion} && ${processorArchitecture}",
                                                ],
                                                testSetup: {
                                                    checkout scm
                                                    unstash 'sdist'
                                                },
                                                retries: 3,
                                                testCommand: {
                                                    findFiles(glob: 'dist/*.tar.gz').each{
                                                        sh(label: 'Running Tox',
                                                           script: """python${pythonVersion} -m venv venv
                                                           ./venv/bin/python -m pip install --upgrade pip
                                                           ./venv/bin/pip install "\$(grep -oE '^tox==.\\S+' ./requirements-dev.txt)"
                                                           ./venv/bin/tox --installpkg ${it.path} -e py${pythonVersion.replace('.', '')}"""
                                                        )
                                                    }
                                                },
                                                post:[
                                                    cleanup: {
                                                        cleanWs(
                                                            patterns: [
                                                                    [pattern: 'dist/', type: 'INCLUDE'],
                                                                    [pattern: 'venv/', type: 'INCLUDE'],
                                                                    [pattern: '.tox/', type: 'INCLUDE'],
                                                                ],
                                                            notFailBuild: true,
                                                            deleteDirs: true
                                                        )
                                                    },
                                                ]
                                            )
                                        }
                                        macTests["Mac ${processorArchitecture} - Python ${pythonVersion}: wheel"] = {
                                            testPythonPkg(
                                                agent: [
                                                    label: "mac && python${pythonVersion} && ${processorArchitecture}",
                                                ],
                                                retries: 3,
                                                testCommand: {
                                                    unstash 'wheel'
                                                    findFiles(glob: 'dist/*.whl').each{
                                                        sh(label: 'Running Tox',
                                                           script: """python${pythonVersion} -m venv venv
                                                                      . ./venv/bin/activate
                                                                      python -m pip install --upgrade pip
                                                                      ./venv/bin/pip install "\$(grep -oE '^tox==.\\S+' ./requirements-dev.txt)"
                                                                      tox --installpkg ${it.path} -e py${pythonVersion.replace('.', '')}
                                                                   """
                                                        )
                                                    }
                                                },
                                                post:[
                                                    cleanup: {
                                                        cleanWs(
                                                            patterns: [
                                                                    [pattern: 'dist/', type: 'INCLUDE'],
                                                                    [pattern: 'venv/', type: 'INCLUDE'],
                                                                    [pattern: '.tox/', type: 'INCLUDE'],
                                                                ],
                                                            notFailBuild: true,
                                                            deleteDirs: true
                                                        )
                                                    },
                                                    success: {
                                                         archiveArtifacts artifacts: 'dist/*.whl'
                                                    }
                                                ]
                                            )
                                        }
                                    }
                                }
                            }
                            parallel(linuxTests + windowsTests + macTests)
                        }
                    }
                }
            }
        }
        stage('Deploy'){
            parallel {
                stage('Deploy to pypi') {
                    agent {
                        dockerfile {
                            filename 'ci/docker/python/linux/jenkins/Dockerfile'
                            label 'linux&&docker'
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
                        unstash 'sdist'
                        unstash 'wheel'
                        pypiUpload(
                            credentialsId: 'jenkins-nexus',
                            repositoryUrl: SERVER_URL,
                            glob: 'dist/*'
                            )
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
                    agent {
                        dockerfile {
                            filename 'ci/docker/python/linux/jenkins/Dockerfile'
                            label 'linux && docker'
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
