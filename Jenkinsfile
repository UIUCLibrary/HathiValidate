@Library("ds-utils")
// Uses https://github.com/UIUCLibrary/Jenkins_utils
import org.ds.*

@Library(["devpi", "PythonHelpers"]) _

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
SUPPORTED_MAC_VERSIONS = ['3.8', '3.9']
SUPPORTED_LINUX_VERSIONS = ['3.6', '3.7', '3.8', '3.9']
SUPPORTED_WINDOWS_VERSIONS = ['3.6', '3.7', '3.8', '3.9']

// ============================================================================
SONARQUBE_CREDENTIAL_ID = 'sonartoken-hathivalidate'

def DEVPI_CONFIG = [
    stagingIndex: getDevPiStagingIndex(),
    server: 'https://devpi.library.illinois.edu',
    credentialsId: 'DS_devpi',
]

DEVPI_STAGING_INDEX = "DS_Jenkins/${getDevPiStagingIndex()}"
defaultParameterValues = [
    USE_SONARQUBE: false
]

def remove_from_devpi(devpiExecutable, pkgName, pkgVersion, devpiIndex, devpiUsername, devpiPassword){
    script {
            try {
                bat "${devpiExecutable} login ${devpiUsername} --password ${devpiPassword}"
                bat "${devpiExecutable} use ${devpiIndex}"
                bat "${devpiExecutable} remove -y ${pkgName}==${pkgVersion}"
            } catch (Exception ex) {
                echo "Failed to remove ${pkgName}==${pkgVersion} from ${devpiIndex}"
        }

    }
}

def CONFIGURATIONS = [
        "3.6" : [
            os: [
                windows:[
                    agents: [
                        build: [
                            dockerfile: [
                                filename: 'ci/docker/python/windows/jenkins/Dockerfile',
                                label: 'windows && docker',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.6-windowsservercore'
                            ]
                        ],
                        test:[
                            dockerfile: [
                                filename: 'ci/docker/python/windows/jenkins/Dockerfile',
                                label: 'windows && docker',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.6-windowsservercore'
                            ]
                        ],
                        devpi: [
                            dockerfile: [
                                filename: 'ci/docker/python/windows/jenkins/Dockerfile',
                                label: 'windows && docker',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.6-windowsservercore'
                            ]
                        ]
                    ],
                    pkgRegex: [
                        wheel: "*.whl",
                        sdist: "*.zip"
                    ]
                ],
                linux: [
                    agents: [
                        build: [
                            dockerfile: [
                                filename: 'ci/docker/python/linux/jenkins/Dockerfile',
                                label: 'linux&&docker',
                                additionalBuildArgs: '--build-arg PYTHON_VERSION=3.6 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                            ]
                        ],
                        test: [
                            dockerfile: [
                                filename: 'ci/docker/python/linux/jenkins/Dockerfile',
                                label: 'linux&&docker',
                                additionalBuildArgs: '--build-arg PYTHON_VERSION=3.6 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                            ]
                        ],
                        devpi: [
                            dockerfile: [
                                filename: 'ci/docker/python/linux/jenkins/Dockerfile',
                                label: 'linux&&docker',
                                additionalBuildArgs: '--build-arg PYTHON_VERSION=3.6 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                            ]
                        ]
                    ],
                    pkgRegex: [
                        wheel: "*.whl",
                        sdist: "*.zip"
                    ]
                ]
            ],
            tox_env: "py36",
            devpiSelector: [
                sdist: "zip",
                wheel: "whl",
            ],
            pkgRegex: [
                wheel: "*.whl",
                sdist: "*.zip"
            ]
        ],
        "3.7" : [
            os: [
                windows: [
                    agents: [
                        build: [
                            dockerfile: [
                                filename: 'ci/docker/python/windows/jenkins/Dockerfile',
                                label: 'windows && docker',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.7'
                            ]
                        ],
                        test: [
                            dockerfile: [
                                filename: 'ci/docker/python/windows/jenkins/Dockerfile',
                                label: 'windows && docker',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.7'
                            ]
                        ],
                        devpi: [
                            dockerfile: [
                                filename: 'ci/docker/python/windows/jenkins/Dockerfile',
                                label: 'windows && docker',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.7'
                            ]
                        ]
                    ],
                    pkgRegex: [
                        wheel: "*.whl",
                        sdist: "*.zip"
                    ]
                ],
                linux: [
                    agents: [
                        build: [
                            dockerfile: [
                                filename: 'ci/docker/python/linux/jenkins/Dockerfile',
                                label: 'linux&&docker',
                                additionalBuildArgs: '--build-arg PYTHON_VERSION=3.7 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                            ]
                        ],
                        test: [
                            dockerfile: [
                                filename: 'ci/docker/python/linux/jenkins/Dockerfile',
                                label: 'linux&&docker',
                                additionalBuildArgs: '--build-arg PYTHON_VERSION=3.7 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                            ]
                        ],
                        devpi: [
                            dockerfile: [
                                filename: 'ci/docker/python/linux/jenkins/Dockerfile',
                                label: 'linux&&docker',
                                additionalBuildArgs: '--build-arg PYTHON_VERSION=3.7 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                            ]
                        ]
                    ],
                    pkgRegex: [
                        wheel: "*.whl",
                        sdist: "*.zip"
                    ]
                ]
            ],
            tox_env: "py37",
            devpiSelector: [
                sdist: "zip",
                wheel: "whl",
            ],
            pkgRegex: [
                wheel: "*.whl",
                sdist: "*.zip"
            ]
        ],
        "3.8" : [
            os: [
                windows: [
                    agents: [
                        build: [
                            dockerfile: [
                                filename: 'ci/docker/python/windows/jenkins/Dockerfile',
                                label: 'windows && docker',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.8'
                            ]
                        ],
                        test: [
                            dockerfile: [
                                filename: 'ci/docker/python/windows/jenkins/Dockerfile',
                                label: 'windows && docker',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.8'
                            ]
                        ],
                        devpi: [
                            dockerfile: [
                                filename: 'ci/docker/python/windows/jenkins/Dockerfile',
                                label: 'windows && docker',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.8'
                            ]
                        ]

                    ],
                    pkgRegex: [
                        wheel: "*.whl",
                        sdist: "*.zip"
                    ]
                ],
                linux: [
                    agents: [
                        build: [
                            dockerfile: [
                                filename: 'ci/docker/python/linux/jenkins/Dockerfile',
                                label: 'linux&&docker',
                                additionalBuildArgs: '--build-arg PYTHON_VERSION=3.8 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                            ]
                        ],
                        test: [
                            dockerfile: [
                                filename: 'ci/docker/python/linux/jenkins/Dockerfile',
                                label: 'linux&&docker',
                                additionalBuildArgs: '--build-arg PYTHON_VERSION=3.8 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                            ]
                        ],
                        devpi: [
                            dockerfile: [
                                filename: 'ci/docker/python/linux/jenkins/Dockerfile',
                                label: 'linux&&docker',
                                additionalBuildArgs: '--build-arg PYTHON_VERSION=3.8 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                            ]
                        ]
                    ],
                    pkgRegex: [
                        wheel: "*.whl",
                        sdist: "*.zip"
                    ]
                ]
            ],
            tox_env: "py38",
            devpiSelector: [
                sdist: "zip",
                wheel: "whl",
            ],
            pkgRegex: [
                wheel: "*.whl",
                sdist: "*.zip"
            ]
        ],
    ]
def get_tox_jobs(){
    sh "tox --workdir .tox -vv -e py"
}

def test_devpi(DevpiPath, DevpiIndex, packageName, PackageRegex, certsDir="certs\\"){

    script{
        bat "${DevpiPath} use ${DevpiIndex} --clientdir ${certsDir}"
        withCredentials([usernamePassword(credentialsId: "DS_devpi", usernameVariable: 'DEVPI_USERNAME', passwordVariable: 'DEVPI_PASSWORD')]) {
           bat "${DevpiPath} login DS_Jenkins --clientdir ${certsDir} --password ${DEVPI_PASSWORD}"
        }
    }
    echo "Testing on ${NODE_NAME}"
    bat "${DevpiPath} test --index ${DevpiIndex} --verbose ${packageName} -s ${PackageRegex} --clientdir ${certsDir} --tox-args=\"-vv\""
}

def get_package_version(stashName, metadataFile){
    ws {
        unstash "${stashName}"
        script{
            def props = readProperties interpolate: true, file: "${metadataFile}"
            deleteDir()
            return props.Version
        }
    }
}

def get_package_name(stashName, metadataFile){
    ws {
        unstash "${stashName}"
        script{
            def props = readProperties interpolate: true, file: "${metadataFile}"
            deleteDir()
            return props.Name
        }
    }
}


def startup(){
    def SONARQUBE_CREDENTIAL_ID = SONARQUBE_CREDENTIAL_ID
    parallel(
        [
            failFast: true,
            'Checking sonarqube Settings': {
                node(){
                    try{
                        withCredentials([string(credentialsId: SONARQUBE_CREDENTIAL_ID, variable: 'dddd')]) {
                            echo 'Found credentials for sonarqube'
                        }
                        defaultParameterValues.USE_SONARQUBE = true
                    } catch(e){
                        echo "Setting defaultValue for USE_SONARQUBE to false. Reason: ${e}"
                        defaultParameterValues.USE_SONARQUBE = false
                    }
                }
            },
            'Getting Distribution Info': {
                node('linux && docker') {
                    timeout(2){
                        ws{
                            checkout scm
                            try{
                                docker.image('python:3.8').inside {
                                    sh(
                                       label: 'Running setup.py with dist_info',
                                       script: '''python --version
                                                  python setup.py dist_info
                                               '''
                                    )
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
        string(name: "PROJECT_NAME", defaultValue: "Hathi Validate", description: "Name given to the project")
        booleanParam(name: 'RUN_CHECKS', defaultValue: false, description: 'Run checks on code')
        booleanParam(name: 'TEST_RUN_TOX', defaultValue: false, description: 'Run Tox Tests')
        booleanParam(name: "BUILD_PACKAGES", defaultValue: true, description: "Build Python packages")
        booleanParam(name: "TEST_PACKAGES", defaultValue: true, description: "Build Python packages")
        booleanParam(name: 'TEST_PACKAGES_ON_MAC', defaultValue: false, description: 'Test Python packages on Mac')
        booleanParam(name: 'USE_SONARQUBE', defaultValue: defaultParameterValues.USE_SONARQUBE, description: 'Send data test data to SonarQube')
        booleanParam(name: "DEPLOY_DEVPI", defaultValue: false, description: "Deploy to devpi on http://devpy.library.illinois.edu/DS_Jenkins/${env.BRANCH_NAME}")
        booleanParam(name: "DEPLOY_DEVPI_PRODUCTION", defaultValue: false, description: "Deploy to https://devpi.library.illinois.edu/production/release")
        booleanParam(name: "DEPLOY_HATHI_TOOL_BETA", defaultValue: false, description: "Deploy standalone to \\\\storage.library.illinois.edu\\HathiTrust\\Tools\\beta\\")
        booleanParam(name: "DEPLOY_DOCS", defaultValue: false, description: "Update online documentation")
        string(name: 'URL_SUBFOLDER', defaultValue: "hathi_validate", description: 'The directory that the docs should be saved under')
    }
    stages {
        stage("Build Documentation"){
            agent {
                dockerfile {
                    filename 'ci/docker/python/linux/jenkins/Dockerfile'
                    label 'linux && docker'
                }
            }
            steps{
                echo "Building docs on ${env.NODE_NAME}"
                sh(script: """mkdir -p logs
                              python -m sphinx -b html docs/source build/docs/html -d build/docs/doctrees -w logs/build_sphinx.log
                           """
                )
            }
            post{
                always {
                    archiveArtifacts artifacts: "logs/build_sphinx.log", allowEmptyArchive: true
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
                            label 'linux && docker'
                            args '--mount source=sonar-cache-hathi_validate,target=/opt/sonar/.sonar/cache'
                        }
                    }
                    stages{
                        stage('Set up Tests') {
                            steps{
                                sh(label: "Adding logs and reports directories",
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
                                stage('Behave') {
                                    steps {
                                        catchError(buildResult: 'UNSTABLE', message: 'Did not pass all Behave BDD tests', stageResult: "UNSTABLE") {
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
                                stage('Pylint') {
                                    steps{
                                        catchError(buildResult: 'SUCCESS', message: 'Pylint found issues', stageResult: 'UNSTABLE') {
                                            sh(label: 'Running pylint',
                                                script: 'pylint hathi_validate -r n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" --persistent=no > reports/pylint.txt'
                                            )
                                        }
                                        sh(
                                            script: 'pylint hathi_validate -r n --msg-template="{path}:{module}:{line}: [{msg_id}({symbol}), {obj}] {msg}" --persistent=no | tee reports/pylint_issues.txt',
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
                                stage("Doctest"){
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
                        stage('Run Sonarqube Analysis'){
                            options{
                                lock('hathivalidate-sonarscanner')
                            }
                            when{
                                equals expected: true, actual: params.USE_SONARQUBE
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
                                        credentialsId: SONARQUBE_CREDENTIAL_ID,
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
                }
                stage("Run Tox"){
                    when{
                        equals expected: true, actual: params.TEST_RUN_TOX
                    }
                    steps {
                        script{
                            def tox

                            node(){
                                checkout scm
                                tox = load("ci/jenkins/scripts/tox.groovy")
                            }

                            def windowsJobs
                            def linuxJobs
                            parallel(
                                "Scanning Tox Environments for Linux":{
                                    linuxJobs = tox.getToxTestsParallel(
                                                envNamePrefix: 'Tox Linux',
                                                label: 'linux && docker',
                                                dockerfile: 'ci/docker/python/linux/tox/Dockerfile',
                                                dockerArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_UR'
                                            )
                                },
                                "Scanning Tox Environments for Windows":{
                                    windowsJobs = tox.getToxTestsParallel(
                                                envNamePrefix: 'Tox Windows',
                                                label: 'windows && docker',
                                                dockerfile: 'ci/docker/python/windows/tox/Dockerfile',
                                                dockerArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg CHOCOLATEY_SOURCE'
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
        stage("Packaging") {
            when{
                anyOf{
                    equals expected: true, actual: params.BUILD_PACKAGES
                    equals expected: true, actual: params.DEPLOY_DEVPI
                    equals expected: true, actual: params.DEPLOY_DEVPI_PRODUCTION
                }
                beforeAgent true
            }
            stages{
                stage("Building Python Distribution Packages"){
                    agent {
                        dockerfile {
                            filename 'ci/docker/python/linux/jenkins/Dockerfile'
                            label 'linux && docker'
                        }
                    }
                    steps{
                        sh(label:'Building Python packages',
                           script: 'python -m pep517.build .'
                           )
                    }
                    post{
                        always{
                            stash includes: 'dist/*.whl', name: "wheel"
                            stash includes: 'dist/*.zip,dist/*.tar.gz', name: "sdist"
                        }
                        success{
                            archiveArtifacts artifacts: "dist/*.whl,dist/*.tar.gz,dist/*.zip", fingerprint: true
                        }
                        cleanup{
                            cleanWs notFailBuild: true
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
                            SUPPORTED_WINDOWS_VERSIONS.each{ pythonVersion ->
                                windowsTests["Windows - Python ${pythonVersion}: sdist"] = {
                                        packages.testPkg(
                                            agent: [
                                                dockerfile: [
                                                    label: 'windows && docker',
                                                    filename: 'ci/docker/python/windows/tox/Dockerfile',
                                                    additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL'
                                                ]
                                            ],
                                            glob: 'dist/*.tar.gz,dist/*.zip',
                                            stash: 'sdist',
                                            pythonVersion: pythonVersion
                                        )
                                    }
                                windowsTests["Windows - Python ${pythonVersion}: wheel"] = {
                                        packages.testPkg(
                                            agent: [
                                                dockerfile: [
                                                    label: 'windows && docker',
                                                    filename: 'ci/docker/python/windows/tox/Dockerfile',
                                                    additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL'
                                                ]
                                            ],
                                            glob: 'dist/*.whl',
                                            stash: 'wheel',
                                            pythonVersion: pythonVersion
                                        )
                                    }
                            }

                            def linuxTests = [:]
                            SUPPORTED_LINUX_VERSIONS.each{ pythonVersion ->
                                linuxTests["Linux - Python ${pythonVersion}: sdist"] = {
                                    packages.testPkg(
                                        agent: [
                                            dockerfile: [
                                                label: 'linux && docker',
                                                filename: 'ci/docker/python/linux/tox/Dockerfile',
                                                additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL'
                                            ]
                                        ],
                                        glob: 'dist/*.tar.gz',
                                        stash: 'sdist',
                                        pythonVersion: pythonVersion
                                    )
                                }
                                linuxTests["Linux - Python ${pythonVersion}: wheel"] = {
                                    packages.testPkg(
                                        agent: [
                                            dockerfile: [
                                                label: 'linux && docker',
                                                filename: 'ci/docker/python/linux/tox/Dockerfile',
                                                additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL'
                                            ]
                                        ],
                                        glob: 'dist/*.whl',
                                        stash: 'wheel',
                                        pythonVersion: pythonVersion
                                    )
                                }
                            }

                            def macTests = [:]
                            SUPPORTED_MAC_VERSIONS.each{ pythonVersion ->
                                macTests["Mac - Python ${pythonVersion}: sdist"] = {
                                    packages.testPkg(
                                            agent: [
                                                label: "mac && python${pythonVersion}",
                                            ],
                                            glob: 'dist/*.tar.gz,dist/*.zip',
                                            stash: 'sdist',
                                            pythonVersion: pythonVersion,
                                            toxExec: 'venv/bin/tox',
                                            testSetup: {
                                                checkout scm
                                                unstash 'sdist'
                                                sh(
                                                    label:'Install Tox',
                                                    script: '''python3 -m venv venv
                                                               venv/bin/pip install pip --upgrade
                                                               venv/bin/pip install tox
                                                               '''
                                                )
                                            },
                                            testTeardown: {
                                                sh 'rm -r venv/'
                                            }

                                        )
                                }
                                macTests["Mac - Python ${pythonVersion}: wheel"] = {
                                    packages.testPkg(
                                            agent: [
                                                label: "mac && python${pythonVersion}",
                                            ],
                                            glob: 'dist/*.whl',
                                            stash: 'wheel',
                                            pythonVersion: pythonVersion,
                                            toxExec: 'venv/bin/tox',
                                            testSetup: {
                                                checkout scm
                                                unstash 'wheel'
                                                sh(
                                                    label:'Install Tox',
                                                    script: '''python3 -m venv venv
                                                               venv/bin/pip install pip --upgrade
                                                               venv/bin/pip install tox
                                                               '''
                                                )
                                            },
                                            testTeardown: {
                                                sh 'rm -r venv/'
                                            }

                                        )
                                }
                            }
                            def tests = linuxTests + windowsTests
                            if(params.TEST_PACKAGES_ON_MAC == true){
                                tests = tests + macTests
                            }
                            parallel(tests)
                        }
                    }
                }
            }
        }
        stage("Deploy to Devpi"){
            when {
                allOf{
                    equals expected: true, actual: params.DEPLOY_DEVPI
                    anyOf {
                        equals expected: "master", actual: env.BRANCH_NAME
                        equals expected: "dev", actual: env.BRANCH_NAME
                        tag '*'
                    }
                }
                beforeAgent true
            }
            agent none
            environment{
                DEVPI = credentials("DS_devpi")
            }
            options{
                lock("HathiValidate-devpi")
            }
            stages{
                stage("Deploy to Devpi Staging") {
                    agent {
                        dockerfile {
                            filename 'ci/docker/python/linux/jenkins/Dockerfile'
                            label 'linux && docker'
                            additionalBuildArgs '--build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                          }
                    }
                    steps {
                        timeout(5){
                            unstash "wheel"
                            unstash "sdist"
                            unstash "DOCUMENTATION"
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
                stage("Test DevPi packages") {
                    matrix {
                        axes {
                            axis {
                                name 'PYTHON_VERSION'
                                values '3.6','3.7', '3.8'
                            }
                            axis {
                                name 'FORMAT'
                                values "wheel", 'sdist'
                            }
                            axis {
                                name 'PLATFORM'
                                values(
                                    "windows",
                                    "linux"
                                )
                            }
                        }
                        excludes{
                             exclude {
                                 axis {
                                     name 'PLATFORM'
                                     values 'linux'
                                 }
                                 axis {
                                     name 'FORMAT'
                                     values 'wheel'
                                 }
                             }
                        }
                        agent none
                        stages{
                            stage("Testing DevPi Package"){
                                agent {
                                  dockerfile {
                                    filename "${CONFIGURATIONS[PYTHON_VERSION].os[PLATFORM].agents.devpi.dockerfile.filename}"
                                    additionalBuildArgs "${CONFIGURATIONS[PYTHON_VERSION].os[PLATFORM].agents.devpi.dockerfile.additionalBuildArgs}"
                                    label "${CONFIGURATIONS[PYTHON_VERSION].os[PLATFORM].agents.devpi.dockerfile.label}"
                                  }
                                }
                                steps{
                                    script{
                                        if(isUnix()){
                                            sh(
                                                label: "Checking Python version",
                                                script: "python --version"
                                            )
                                            sh(
                                                label: "Connecting to DevPi index",
                                                script: "devpi use https://devpi.library.illinois.edu --clientdir certs && devpi login $DEVPI_USR --password $DEVPI_PSW --clientdir certs && devpi use ${env.BRANCH_NAME}_staging --clientdir certs"
                                            )
                                            sh(
                                                label: "Running tests on Devpi",
                                                script: "devpi test --index ${env.BRANCH_NAME}_staging ${props.Name}==${props.Version} -s ${CONFIGURATIONS[PYTHON_VERSION].devpiSelector[FORMAT]} --clientdir certs -e ${CONFIGURATIONS[PYTHON_VERSION].tox_env} -v"
                                            )
                                        } else {
                                            bat(
                                                label: "Checking Python version",
                                                script: "python --version"
                                            )
                                            bat(
                                                label: "Connecting to DevPi index",
                                                script: "devpi use https://devpi.library.illinois.edu --clientdir certs\\ && devpi login %DEVPI_USR% --password %DEVPI_PSW% --clientdir certs\\ && devpi use ${env.BRANCH_NAME}_staging --clientdir certs\\"
                                            )
                                            bat(
                                                label: "Running tests on Devpi",
                                                script: "devpi test --index ${env.BRANCH_NAME}_staging ${props.Name}==${props.Version} -s ${CONFIGURATIONS[PYTHON_VERSION].devpiSelector[FORMAT]} --clientdir certs\\ -e ${CONFIGURATIONS[PYTHON_VERSION].tox_env} -v"
                                            )
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
                stage("Deploy to DevPi Production") {
                    when {
                        allOf{
                            equals expected: true, actual: params.DEPLOY_DEVPI_PRODUCTION
                            anyOf {
                                equals expected: 'master', actual: env.BRANCH_NAME
                                tag '*'
                            }
                        }
                        beforeAgent true
                    }
                    agent {
                        dockerfile {
                            filename 'ci/docker/python/linux/jenkins/Dockerfile'
                            label 'linux&&docker'
                            additionalBuildArgs '--build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                        }
                    }
                    steps {
                        script {
                            try{
                                timeout(30) {
                                    input "Release ${props.Name} ${props.Version} (https://devpi.library.illinois.edu/DS_Jenkins/${env.BRANCH_NAME}_staging/${props.Name}/${props.Version}) to DevPi Production? "
                                }
                                sh "devpi use https://devpi.library.illinois.edu --clientdir ${WORKSPACE}/devpi  && devpi login $DEVPI_USR --password $DEVPI_PSW --clientdir ${WORKSPACE}/devpi && devpi use /DS_Jenkins/${env.BRANCH_NAME}_staging --clientdir ${WORKSPACE}/devpi && devpi push --index ${env.DEVPI_USR}/${env.BRANCH_NAME}_staging ${props.Name}==${props.Version} production/release --clientdir ${WORKSPACE}/devpi"
                            } catch(err){
                                echo "User response timed out. Packages not deployed to DevPi Production."
                            }
                        }
                    }
                }
            }
            post{
                success{
                    node('linux && docker') {
                        checkout scm
                        script{
                            docker.build("hathivalidate:devpi",'-f ./ci/docker/python/linux/jenkins/Dockerfile --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) .').inside{
                                sh(
                                    label: "Connecting to DevPi Server",
                                    script: 'devpi use https://devpi.library.illinois.edu --clientdir ${WORKSPACE}/devpi && devpi login $DEVPI_USR --password $DEVPI_PSW --clientdir ${WORKSPACE}/devpi'
                                )
                                sh "devpi use /DS_Jenkins/${env.BRANCH_NAME}_staging --clientdir ${WORKSPACE}/devpi"
                                sh "devpi push ${props.Name}==${props.Version} DS_Jenkins/${env.BRANCH_NAME} --clientdir ${WORKSPACE}/devpi"
                            }
                        }
                    }
                }
                cleanup{
                    node('linux && docker') {
                       script{
                            docker.build("hathivalidate:devpi",'-f ./ci/docker/python/linux/jenkins/Dockerfile --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) .').inside{
                                sh(
                                    label: "Connecting to DevPi Server",
                                    script: 'devpi use https://devpi.library.illinois.edu --clientdir ${WORKSPACE}/devpi && devpi login $DEVPI_USR --password $DEVPI_PSW --clientdir ${WORKSPACE}/devpi'
                                )
                                sh "devpi use /DS_Jenkins/${env.BRANCH_NAME}_staging --clientdir ${WORKSPACE}/devpi"
                                sh "devpi remove -y ${props.Name}==${props.Version} --clientdir ${WORKSPACE}/devpi"
                            }
                       }
                    }
                }
            }
        }
        stage("Deploy"){
            parallel {
                stage("Deploy Online Documentation") {
                    agent{
                        label "!aws"
                    }
                    when{
                        equals expected: true, actual: params.DEPLOY_DOCS
                        beforeAgent true
                    }
                    steps{
                        unstash "DOCUMENTATION"
                        dir("build/docs/html/"){
                            input 'Update project documentation?'
                            sshPublisher(
                                publishers: [
                                    sshPublisherDesc(
                                        configName: 'apache-ns - lib-dccuser-updater',
                                        sshLabel: [label: 'Linux'],
                                        transfers: [sshTransfer(excludes: '',
                                        execCommand: '',
                                        execTimeout: 120000,
                                        flatten: false,
                                        makeEmptyDirs: false,
                                        noDefaultExcludes: false,
                                        patternSeparator: '[, ]+',
                                        remoteDirectory: "${params.DEPLOY_DOCS_URL_SUBFOLDER}",
                                        remoteDirectorySDF: false,
                                        removePrefix: '',
                                        sourceFiles: '**')],
                                    usePromotionTimestamp: false,
                                    useWorkspaceInPromotion: false,
                                    verbose: true
                                    )
                                ]
                            )
                        }
                    }
                }

            }
        }
    }
}
