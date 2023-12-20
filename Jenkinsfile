
def getDevPiStagingIndex(){
    if (env.TAG_NAME?.trim()){
        return 'tag_staging'
    } else{
        return "${env.BRANCH_NAME}_staging"
    }
}

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

def getDevpiConfig() {
    node(){
        configFileProvider([configFile(fileId: 'devpi_config', variable: 'CONFIG_FILE')]) {
            def configProperties = readProperties(file: CONFIG_FILE)
            configProperties.stagingIndex = {
                if (env.TAG_NAME?.trim()){
                    return 'tag_staging'
                } else{
                    return "${env.BRANCH_NAME}_staging"
                }
            }()
            return configProperties
        }
    }
}
def DEVPI_CONFIG = getDevpiConfig()

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
def get_props(){
    stage('Reading Package Metadata'){
        node(){
            unstash 'DIST-INFO'
            def metadataFile = findFiles( glob: '*.dist-info/METADATA')[0]
            def metadata = readProperties(interpolate: true, file: metadataFile.path )
            echo """Version = ${metadata.Version}
Name = ${metadata.Name}
"""
            return metadata
        }
    }
}

node(){
    checkout scm
    devpi = load('ci/jenkins/scripts/devpi.groovy')
}


startup()
def props = get_props()
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
        booleanParam(name: 'DEPLOY_DEVPI', defaultValue: false, description: "Deploy to devpi on http://devpy.library.illinois.edu/DS_Jenkins/${env.BRANCH_NAME}")
        booleanParam(name: 'DEPLOY_PYPI', defaultValue: false, description: 'Deploy to pypi')
        booleanParam(name: 'DEPLOY_DEVPI_PRODUCTION', defaultValue: false, description: 'Deploy to https://devpi.library.illinois.edu/production/release')
        booleanParam(name: 'DEPLOY_HATHI_TOOL_BETA', defaultValue: false, description: 'Deploy standalone to \\\\storage.library.illinois.edu\\HathiTrust\\Tools\\beta\\')
        booleanParam(name: 'DEPLOY_DOCS', defaultValue: false, description: 'Update online documentation')
    }
    stages {
        stage('Building and Testing'){
            when{
                anyOf{
                    equals expected: true, actual: params.RUN_CHECKS
                    equals expected: true, actual: params.TEST_RUN_TOX
                    equals expected: true, actual: params.DEPLOY_DEVPI
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
                    when{
                        anyOf{
                            equals expected: true, actual: params.RUN_CHECKS
                            equals expected: true, actual: params.DEPLOY_DEVPI
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
                                zip archive: true, dir: 'build/docs/html', glob: '', zipFile: "dist/${props.Name}-${props.Version}.doc.zip"
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
                                            publishCoverage(
                                                adapters: [
                                                        coberturaAdapter('reports/coverage.xml')
                                                    ],
                                                sourceFileResolver: sourceFiles('STORE_ALL_BUILD')
                                            )
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
                                                        version: props.Version,
                                                        name: props.Name
                                                    ],
                                                )
                                            } else {
                                                sonarqube.submitToSonarcloud(
                                                    reportStashes: stashes,
                                                    artifactStash: 'sonarqube artifacts',
                                                    sonarqube: sonarqubeConfig,
                                                    package: [
                                                        version: props.Version,
                                                        name: props.Name
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
                stage('Run Tox'){
                    when{
                        equals expected: true, actual: params.TEST_RUN_TOX
                    }
                    steps {
                        script{
                            def tox = fileLoader.fromGit(
                                'tox',
                                'https://github.com/UIUCLibrary/jenkins_helper_scripts.git',
                                '8',
                                null,
                                ''
                            )

                            def windowsJobs
                            def linuxJobs
                            parallel(
                                'Scanning Tox Environments for Linux':{
                                    linuxJobs = tox.getToxTestsParallel(
                                                envNamePrefix: 'Tox Linux',
                                                label: 'linux && docker && x86',
                                                dockerfile: 'ci/docker/python/linux/tox/Dockerfile',
                                                dockerArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg PIP_DOWNLOAD_CACHE=/.cache/pip',
                                                dockerRunArgs: '-v pipcache_hathivalidate:/.cache/pip',
                                                retry: 2
                                            )
                                },
                                'Scanning Tox Environments for Windows':{
                                    windowsJobs = tox.getToxTestsParallel(
                                                envNamePrefix: 'Tox Windows',
                                                label: 'windows && docker && x86',
                                                dockerfile: 'ci/docker/python/windows/tox/Dockerfile',
                                                dockerArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg CHOCOLATEY_SOURCE --build-arg PIP_DOWNLOAD_CACHE=c:/users/containeradministrator/appdata/local/pip',
                                                dockerRunArgs: '-v pipcache_hathivalidate:c:/users/containeradministrator/appdata/local/pip',
                                                retry: 2
                                            )
                                },
                                failFast: true
                            )
                            parallel(windowsJobs + linuxJobs)
                        }
                    }
                }
            }
        }
        stage('Packaging') {
            when{
                anyOf{
                    equals expected: true, actual: params.BUILD_PACKAGES
                    equals expected: true, actual: params.DEPLOY_DEVPI
                    equals expected: true, actual: params.DEPLOY_DEVPI_PRODUCTION
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
                            def packages
                            node(){
                                checkout scm
                                packages = load 'ci/jenkins/scripts/packaging.groovy'
                            }
                            def windowsTests = [:]
                            if(params.INCLUDE_WINDOWS_X86_64 == true){
                                SUPPORTED_WINDOWS_VERSIONS.each{ pythonVersion ->
                                    windowsTests["Windows - Python ${pythonVersion}: sdist"] = {
                                        packages.testPkg(
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
                                        packages.testPkg(
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
                                        packages.testPkg(
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
                                        packages.testPkg(
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
                                            packages.testPkg(
                                                agent: [
                                                    label: "mac && python${pythonVersion} && ${processorArchitecture}",
                                                ],
                                                testSetup: {
                                                    checkout scm
                                                    unstash 'sdist'
                                                },
                                                testCommand: {
                                                    findFiles(glob: 'dist/*.tar.gz').each{
                                                        sh(label: 'Running Tox',
                                                           script: """python${pythonVersion} -m venv venv
                                                           ./venv/bin/python -m pip install --upgrade pip
                                                           ./venv/bin/pip install -r requirements/requirements_tox.txt
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
                                            packages.testPkg(
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
                                                                      pip install -r requirements/requirements_tox.txt
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
        stage('Deploy to Devpi'){
            when {
                allOf{
                    equals expected: true, actual: params.DEPLOY_DEVPI
                    anyOf {
                        equals expected: 'master', actual: env.BRANCH_NAME
                        equals expected: 'dev', actual: env.BRANCH_NAME
                        tag '*'
                    }
                }
                beforeAgent true
            }
            agent none
            options{
                lock("HathiValidate-devpi")
            }
            stages{
                stage('Deploy to Devpi Staging') {
                    agent {
                        dockerfile {
                            filename 'ci/docker/python/linux/tox/Dockerfile'
                            label 'linux && docker && devpi-access'
                            additionalBuildArgs '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg PIP_DOWNLOAD_CACHE=/.cache/pip'
                          }
                    }
                    steps {
                        timeout(5){
                            unstash 'wheel'
                            unstash 'sdist'
                            unstash 'DOCUMENTATION'
                            script{
                                devpi.upload(
                                        server: DEVPI_CONFIG.server,
                                        credentialsId: DEVPI_CONFIG.credentialsId,
                                        index: DEVPI_CONFIG.stagingIndex,
                                        clientDir: './devpi'
                                    )
                            }
                        }
                    }
                }
                stage('Test DevPi packages') {
                    steps{
                        script{
                            def macPackages = [:]
                            SUPPORTED_MAC_VERSIONS.each{pythonVersion ->
                                def macArchitectures = []
                                if(params.INCLUDE_MACOS_X86_64 == true){
                                    macArchitectures.add('x86_64')
                                }
                                if(params.INCLUDE_MACOS_ARM == true){
                                    macArchitectures.add('arm64')
                                }
                                macArchitectures.each{ processorArchitecture ->
                                    if (nodesByLabel("mac && ${processorArchitecture} && python${pythonVersion}").size() > 0){
                                        macPackages["Test Python ${pythonVersion}: wheel Mac ${processorArchitecture}"] = {
                                            retry(2){
                                                withEnv(['PATH+EXTRA=./venv/bin']) {
                                                    devpi.testDevpiPackage(
                                                        agent: [
                                                            label: "mac && python${pythonVersion} && ${processorArchitecture} && devpi-access"
                                                        ],
                                                        devpi: [
                                                            index: DEVPI_CONFIG.stagingIndex,
                                                            server: DEVPI_CONFIG.server,
                                                            credentialsId: DEVPI_CONFIG.credentialsId,
                                                            devpiExec: 'venv/bin/devpi'
                                                        ],
                                                        package:[
                                                            name: props.Name,
                                                            version: props.Version,
                                                            selector: 'whl'
                                                        ],
                                                        test:[
                                                            setup: {
                                                                checkout scm
                                                                sh(
                                                                    label:'Installing Devpi client',
                                                                    script: '''python3 -m venv venv
                                                                                venv/bin/python -m pip install pip --upgrade
                                                                                venv/bin/python -m pip install 'devpi-client<7.0'  -r requirements/requirements_tox.txt
                                                                                '''
                                                                )
                                                            },
                                                            toxEnv: "py${pythonVersion}".replace('.',''),
                                                            teardown: {
                                                                sh( label: 'Remove Devpi client', script: 'rm -r venv')
                                                            }
                                                        ]
                                                    )
                                                }
                                            }
                                        }
                                        macPackages["Test Python ${pythonVersion}: sdist Mac ${processorArchitecture}"]= {
                                            retry(2){
                                                withEnv(['PATH+EXTRA=./venv/bin']) {
                                                    devpi.testDevpiPackage(
                                                        agent: [
                                                            label: "mac && python${pythonVersion} && ${processorArchitecture} && devpi-access"
                                                        ],
                                                        devpi: [
                                                            index: DEVPI_CONFIG.stagingIndex,
                                                            server: DEVPI_CONFIG.server,
                                                            credentialsId: DEVPI_CONFIG.credentialsId,
                                                            devpiExec: 'venv/bin/devpi'
                                                        ],
                                                        package:[
                                                            name: props.Name,
                                                            version: props.Version,
                                                            selector: 'tar.gz'
                                                        ],
                                                        test:[
                                                            setup: {
                                                                checkout scm
                                                                sh(
                                                                    label:'Installing Devpi client',
                                                                    script: '''python3 -m venv venv
                                                                                venv/bin/python -m pip install pip --upgrade
                                                                                venv/bin/python -m pip install 'devpi-client<7.0'  -r requirements/requirements_tox.txt
                                                                                '''
                                                                )
                                                            },
                                                            toxEnv: "py${pythonVersion}".replace('.',''),
                                                            teardown: {
                                                                sh( label: 'Remove Devpi client', script: 'rm -r venv')
                                                            }
                                                        ]
                                                    )
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                            def windowsPackages = [:]
                            SUPPORTED_WINDOWS_VERSIONS.each{pythonVersion ->
                                windowsPackages["Test Python ${pythonVersion}: sdist Windows"] = {
                                    devpi.testDevpiPackage(
                                        agent: [
                                            dockerfile: [
                                                filename: 'ci/docker/python/windows/tox/Dockerfile',
                                                additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg CHOCOLATEY_SOURCE --build-arg PIP_DOWNLOAD_CACHE=/.cache/pip',
                                                label: 'windows && docker && x86 && devpi-access',
                                                args: '-v pipcache_hathivalidate:c:/users/containeradministrator/appdata/local/pip'
                                            ]
                                        ],
                                        devpi: [
                                            index: DEVPI_CONFIG.stagingIndex,
                                            server: DEVPI_CONFIG.server,
                                            credentialsId: DEVPI_CONFIG.credentialsId,
                                        ],
                                        package:[
                                            name: props.Name,
                                            version: props.Version,
                                            selector: 'tar.gz'
                                        ],
                                        test:[
                                            toxEnv: "py${pythonVersion}".replace('.',''),
                                        ],
                                        retry: 3
                                    )
                                }
                                windowsPackages["Test Python ${pythonVersion}: wheel Windows"] = {
                                    devpi.testDevpiPackage(
                                        agent: [
                                            dockerfile: [
                                                filename: 'ci/docker/python/windows/tox/Dockerfile',
                                                additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg CHOCOLATEY_SOURCE --build-arg PIP_DOWNLOAD_CACHE=/.cache/pip',
                                                label: 'windows && docker && x86 && devpi-access',
                                                args: '-v pipcache_hathivalidate:c:/users/containeradministrator/appdata/local/pip'
                                            ]
                                        ],
                                        devpi: [
                                            index: DEVPI_CONFIG.stagingIndex,
                                            server: DEVPI_CONFIG.server,
                                            credentialsId: DEVPI_CONFIG.credentialsId,
                                        ],
                                        package:[
                                            name: props.Name,
                                            version: props.Version,
                                            selector: 'whl'
                                        ],
                                        test:[
                                            toxEnv: "py${pythonVersion}".replace('.',''),
                                        ],
                                        retry: 3
                                    )
                                }
                            }
                            def linuxPackages = [:]
                            SUPPORTED_LINUX_VERSIONS.each{pythonVersion ->
                                if(params.INCLUDE_LINUX_X86_64 == true){
                                    linuxPackages["Test Python ${pythonVersion}: sdist Linux"] = {
                                        devpi.testDevpiPackage(
                                            agent: [
                                                dockerfile: [
                                                    filename: 'ci/docker/python/linux/tox/Dockerfile',
                                                    additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg PIP_DOWNLOAD_CACHE=/.cache/pip',
                                                    label: 'linux && docker && x86 && devpi-access',
                                                    args: '-v pipcache_hathivalidate:/.cache/pip',
                                                ]
                                            ],
                                            devpi: [
                                                index: DEVPI_CONFIG.stagingIndex,
                                                server: DEVPI_CONFIG.server,
                                                credentialsId: DEVPI_CONFIG.credentialsId,
                                            ],
                                            package:[
                                                name: props.Name,
                                                version: props.Version,
                                                selector: 'tar.gz'
                                            ],
                                            test:[
                                                toxEnv: "py${pythonVersion}".replace('.',''),
                                            ],
                                            retry: 3
                                        )
                                    }
                                    linuxPackages["Test Python ${pythonVersion}: wheel Linux"] = {
                                        devpi.testDevpiPackage(
                                            agent: [
                                                dockerfile: [
                                                    filename: 'ci/docker/python/linux/tox/Dockerfile',
                                                    additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg PIP_DOWNLOAD_CACHE=/.cache/pip',
                                                    label: 'linux && docker && x86 && devpi-access',
                                                    args: '-v pipcache_hathivalidate:/.cache/pip',
                                                ]
                                            ],
                                            devpi: [
                                                index: DEVPI_CONFIG.stagingIndex,
                                                server: DEVPI_CONFIG.server,
                                                credentialsId: DEVPI_CONFIG.credentialsId,
                                            ],
                                            package:[
                                                name: props.Name,
                                                version: props.Version,
                                                selector: 'whl'
                                            ],
                                            test:[
                                                toxEnv: "py${pythonVersion}".replace('.',''),
                                            ],
                                            retry: 3
                                        )
                                    }
                                }
                            }
                            parallel(macPackages + windowsPackages + linuxPackages)
                        }
                    }
                }
                stage('Deploy to DevPi Production') {
                    when {
                        allOf{
                            equals expected: true, actual: params.DEPLOY_DEVPI_PRODUCTION
                            anyOf {
                                equals expected: 'master', actual: env.BRANCH_NAME
                                tag '*'
                            }
                        }
                        beforeAgent true
                        beforeInput true
                    }
                    agent {
                        dockerfile {
                            filename 'ci/docker/python/linux/tox/Dockerfile'
                            label 'linux && docker && devpi-access'
                            additionalBuildArgs '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg PIP_DOWNLOAD_CACHE=/.cache/pip'
                        }
                    }
                    input {
                        message 'Release to DevPi Production?'
                    }
                    steps {
                        script{
                            devpi.pushPackageToIndex(
                                pkgName: props.Name,
                                pkgVersion: props.Version,
                                server: DEVPI_CONFIG.server,
                                indexSource: DEVPI_CONFIG.stagingIndex,
                                indexDestination: 'production/release',
                                credentialsId: DEVPI_CONFIG.credentialsId
                            )
                        }
                    }
                }
            }
            post{
                success{
                    node('linux && docker && devpi-access') {
                        checkout scm
                        script{
                            if (!env.TAG_NAME?.trim()){
                                def dockerImage = docker.build('hathivalidate:devpi','-f ./ci/docker/python/linux/tox/Dockerfile --build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg PIP_DOWNLOAD_CACHE=/.cache/pip .')
                                dockerImage.inside{
                                    devpi.pushPackageToIndex(
                                        pkgName: props.Name,
                                        pkgVersion: props.Version,
                                        server: DEVPI_CONFIG.server,
                                        indexSource: DEVPI_CONFIG.stagingIndex,
                                        indexDestination: "DS_Jenkins/${env.BRANCH_NAME}",
                                        credentialsId: DEVPI_CONFIG.credentialsId
                                    )
                                }
                                sh script: "docker image rm --no-prune ${dockerImage.imageName()}"
                            }
                        }
                    }
                }
                cleanup{
                    node('linux && docker && devpi-access') {
                       script{
                            def dockerImage = docker.build('hathivalidate:devpi','-f ./ci/docker/python/linux/tox/Dockerfile --build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg PIP_DOWNLOAD_CACHE=/.cache/pip .')
                            dockerImage.inside{
                                devpi.removePackage(
                                    pkgName: props.Name,
                                    pkgVersion: props.Version,
                                    index: DEVPI_CONFIG.stagingIndex,
                                    server: DEVPI_CONFIG.server,
                                    credentialsId: DEVPI_CONFIG.credentialsId,
                                )
                            }
                            sh script: "docker image rm --no-prune ${dockerImage.imageName()}"
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
                        script{
                            def pypi = fileLoader.fromGit(
                                    'pypi',
                                    'https://github.com/UIUCLibrary/jenkins_helper_scripts.git',
                                    '2',
                                    null,
                                    ''
                                )
                            pypi.pypiUpload(
                                credentialsId: 'jenkins-nexus',
                                repositoryUrl: SERVER_URL,
                                glob: 'dist/*'
                                )
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
