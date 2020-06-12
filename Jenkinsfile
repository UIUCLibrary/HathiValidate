@Library("ds-utils")
// Uses https://github.com/UIUCLibrary/Jenkins_utils
import org.ds.*

@Library(["devpi", "PythonHelpers"]) _
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
                                filename: 'ci/docker/python/windows/Dockerfile',
                                label: 'Windows&&Docker',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.6-windowsservercore'
                            ]
                        ],
                        test:[
                            wheel: [
                                dockerfile: [
                                    filename: 'ci/docker/python/windows/Dockerfile',
                                    label: 'Windows&&Docker',
                                    additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.6-windowsservercore'
                                ]
                            ],
                            sdist: [
                                dockerfile: [
                                    filename: 'ci/docker/python/windows/Dockerfile',
                                    label: 'Windows&&Docker',
                                    additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.6-windowsservercore'
                                ]
                            ]
                        ],
                        devpi: [
                            wheel: [
                                dockerfile: [
                                    filename: 'ci/docker/deploy/devpi/test/windows/whl/Dockerfile',
                                    label: 'Windows&&Docker',
                                    additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.6-windowsservercore'
                                ]
                            ],
                            sdist: [
                                dockerfile: [
                                    filename: 'ci/docker/deploy/devpi/test/windows/source/Dockerfile',
                                    label: 'Windows&&Docker',
                                    additionalBuildArgs: '--build-arg PYTHON_INSTALLER_URL=https://www.python.org/ftp/python/3.6.8/python-3.6.8-amd64.exe --build-arg CHOCOLATEY_SOURCE'
                                ]
                            ]
                        ]
                    ],
                    pkgRegex: [
                        wheel: "*cp36*.whl",
                        sdist: "*.zip"
                    ]
                ],
                linux: [
                    agents: [
                        build: [
                            dockerfile: [
                                filename: 'ci/docker/python/linux/Dockerfile',
                                label: 'linux&&docker',
                                additionalBuildArgs: '--build-arg PYTHON_VERSION=3.6 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                            ]
                        ],
                        test: [
                            sdist: [
                                dockerfile: [
                                    filename: 'ci/docker/python/linux/Dockerfile',
                                    label: 'linux&&docker',
                                    additionalBuildArgs: '--build-arg PYTHON_VERSION=3.6 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                                ]
                            ]
                        ],
                        devpi: [
                            whl: [
                                dockerfile: [
                                    filename: 'ci/docker/deploy/devpi/test/linux/Dockerfile',
                                    label: 'linux&&docker',
                                    additionalBuildArgs: '--build-arg PYTHON_VERSION=3.6 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                                ]
                            ],
                            sdist: [
                                dockerfile: [
                                    filename: 'ci/docker/deploy/devpi/test/linux/Dockerfile',
                                    label: 'linux&&docker',
                                    additionalBuildArgs: '--build-arg PYTHON_VERSION=3.6 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                                ]
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
                wheel: "*.whl",
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
                                filename: 'ci/docker/python/windows/Dockerfile',
                                label: 'Windows&&Docker',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.7'
                            ]
                        ],
                        test: [
                            sdist: [
                                dockerfile: [
                                    filename: 'ci/docker/python/windows/Dockerfile',
                                    label: 'Windows&&Docker',
                                    additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.7'
                                ]
                            ],
                            wheel: [
                                dockerfile: [
                                    filename: 'ci/docker/python/windows/Dockerfile',
                                    additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.7',
                                    label: 'windows && docker',
                                ]
                            ]
                        ],
                        devpi: [
                            wheel: [
                                dockerfile: [
                                    filename: 'ci/docker/deploy/devpi/test/windows/whl/Dockerfile',
                                    label: 'Windows&&Docker',
                                    additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.7'
                                ]
                            ],
                            sdist: [
                                dockerfile: [
                                    filename: 'ci/docker/deploy/devpi/test/windows/source/Dockerfile',
                                    label: 'Windows&&Docker',
                                    additionalBuildArgs: '--build-arg PYTHON_INSTALLER_URL=https://www.python.org/ftp/python/3.7.5/python-3.7.5-amd64.exe --build-arg CHOCOLATEY_SOURCE'
                                ]
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
                                filename: 'ci/docker/python/linux/Dockerfile',
                                label: 'linux&&docker',
                                additionalBuildArgs: '--build-arg PYTHON_VERSION=3.7 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                            ]
                        ],
                        test: [
                            sdist: [
                                dockerfile: [
                                    filename: 'ci/docker/python/linux/Dockerfile',
                                    label: 'linux&&docker',
                                    additionalBuildArgs: '--build-arg PYTHON_VERSION=3.7 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                                ]
                            ]
                        ],
                        devpi: [
                            wheel: [
                                dockerfile: [
                                    filename: 'ci/docker/deploy/devpi/test/linux/Dockerfile',
                                    label: 'linux&&docker',
                                    additionalBuildArgs: '--build-arg PYTHON_VERSION=3.7 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                                ]
                            ],
                            sdist: [
                                dockerfile: [
                                    filename: 'ci/docker/deploy/devpi/test/linux/Dockerfile',
                                    label: 'linux&&docker',
                                    additionalBuildArgs: '--build-arg PYTHON_VERSION=3.7 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                                ]
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
                wheel: "*.whl",
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
                                filename: 'ci/docker/python/windows/Dockerfile',
                                label: 'Windows&&Docker',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.8'
                            ]
                        ],
                        test: [
                            sdist: [
                                dockerfile: [
                                    filename: 'ci/docker/python/windows/Dockerfile',
                                    label: 'Windows&&Docker',
                                    additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.8'
                                ]
                            ],
                            wheel: [
                                dockerfile: [
                                    filename: 'ci/docker/python/windows/Dockerfile',
                                    additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.8',
                                    label: 'windows && docker',
                                ]
                            ]
                        ],
                        devpi: [
                            wheel: [
                                dockerfile: [
                                    filename: 'ci/docker/deploy/devpi/test/windows/whl/Dockerfile',
                                    label: 'Windows&&Docker',
                                    additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.8'
                                ]
                            ],
                            sdist: [
                                dockerfile: [
                                    filename: 'ci/docker/deploy/devpi/test/windows/source/Dockerfile',
                                    label: 'Windows&&Docker',
                                    additionalBuildArgs: '--build-arg PYTHON_INSTALLER_URL=https://www.python.org/ftp/python/3.8.3/python-3.8.3-amd64.exe --build-arg CHOCOLATEY_SOURCE'
                                ]
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
                                filename: 'ci/docker/python/linux/Dockerfile',
                                label: 'linux&&docker',
                                additionalBuildArgs: '--build-arg PYTHON_VERSION=3.8 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                            ]
                        ],
                        test: [
                            sdist: [
                                dockerfile: [
                                    filename: 'ci/docker/python/linux/Dockerfile',
                                    label: 'linux&&docker',
                                    additionalBuildArgs: '--build-arg PYTHON_VERSION=3.8 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                                ]
                            ]
                        ],
                        devpi: [
                            wheel: [
                                dockerfile: [
                                    filename: 'ci/docker/deploy/devpi/test/linux/Dockerfile',
                                    label: 'linux&&docker',
                                    additionalBuildArgs: '--build-arg PYTHON_VERSION=3.8 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                                ]
                            ],
                            sdist: [
                                dockerfile: [
                                    filename: 'ci/docker/deploy/devpi/test/linux/Dockerfile',
                                    label: 'linux&&docker',
                                    additionalBuildArgs: '--build-arg PYTHON_VERSION=3.8 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                                ]
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
                wheel: "*.whl",
            ],
            pkgRegex: [
                wheel: "*.whl",
                sdist: "*.zip"
            ]
        ],
    ]

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



pipeline {
    agent none

    options {
        disableConcurrentBuilds()  //each branch has 1 job running at a time
        buildDiscarder logRotator(artifactDaysToKeepStr: '10', artifactNumToKeepStr: '10')
    }
    triggers {
        cron('@daily')
    }

    parameters {
        string(name: "PROJECT_NAME", defaultValue: "Hathi Validate", description: "Name given to the project")
        booleanParam(name: "TEST_RUN_TOX", defaultValue: true, description: "Run Tox Tests")
        booleanParam(name: "DEPLOY_DEVPI", defaultValue: false, description: "Deploy to devpi on http://devpy.library.illinois.edu/DS_Jenkins/${env.BRANCH_NAME}")
        booleanParam(name: "DEPLOY_DEVPI_PRODUCTION", defaultValue: false, description: "Deploy to https://devpi.library.illinois.edu/production/release")
        booleanParam(name: "DEPLOY_HATHI_TOOL_BETA", defaultValue: false, description: "Deploy standalone to \\\\storage.library.illinois.edu\\HathiTrust\\Tools\\beta\\")
        booleanParam(name: "DEPLOY_DOCS", defaultValue: false, description: "Update online documentation")
        string(name: 'URL_SUBFOLDER', defaultValue: "hathi_validate", description: 'The directory that the docs should be saved under')
    }
    stages {
        stage("Getting Distribution Info"){
            agent {
                dockerfile {
                    filename 'ci/docker/python/linux/Dockerfile'
                    label 'linux && docker'
                }
            }
            steps{
                timeout(4){
                    sh "python setup.py dist_info"
                }
            }
            post{
                success{
                    stash includes: "HathiValidate.dist-info/**", name: 'DIST-INFO'
                    archiveArtifacts artifacts: "HathiValidate.dist-info/**"
                }
            }
        }
        stage("Build"){
            parallel{
                stage("Python Package"){
                    agent {
                        dockerfile {
                            filename 'ci/docker/python/linux/Dockerfile'
                            label 'linux && docker'
                        }
                    }
                    steps {
                        timeout(4){
                            sh "python setup.py build -b build"
                        }
                    }
                }
                stage("Docs"){
                    agent {
                        dockerfile {
                            filename 'ci/docker/python/linux/Dockerfile'
                            label 'linux && docker'
                        }
                    }
                    environment{
                        PKG_NAME = get_package_name("DIST-INFO", "HathiValidate.dist-info/METADATA")
                        PKG_VERSION = get_package_version("DIST-INFO", "HathiValidate.dist-info/METADATA")
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
                        }
                        success{
                            publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'build/docs/html', reportFiles: 'index.html', reportName: 'Documentation', reportTitles: ''])
                            script{
                                def DOC_ZIP_FILENAME = "${env.PKG_NAME}-${env.PKG_VERSION}.doc.zip"
                                zip archive: true, dir: "build/docs/html", glob: '', zipFile: "dist/${DOC_ZIP_FILENAME}"
                                stash includes: "build/docs/**,dist/${DOC_ZIP_FILENAME}", name: "DOCUMENTATION"
                            }
                        }
                        cleanup{
                            cleanWs notFailBuild: true
                        }
                    }
                }
            }
        }
        stage("Tests") {
            parallel {
                stage("PyTest"){
                    agent {
                        dockerfile {
                            filename 'ci/docker/python/linux/Dockerfile'
                            label 'linux && docker'
                        }
                    }
                    steps{
                        sh "python -m pytest --junitxml=reports/junit-${env.NODE_NAME}-pytest.xml --junit-prefix=${env.NODE_NAME}-pytest --cov-report html:reports/coverage/ --cov=hathi_validate" //  --basetemp={envtmpdir}"

                    }
                    post {
                        always{
                            junit "reports/junit-${env.NODE_NAME}-pytest.xml"
                            publishHTML([allowMissing: true, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'reports/coverage', reportFiles: 'index.html', reportName: 'Coverage', reportTitles: ''])
                        }
                    }
                }
                stage("Run Tox"){
                    agent {
                        dockerfile {
                            filename 'ci/docker/python/linux/Dockerfile'
                            label 'linux && docker'
                        }
                    }
                    environment{
                        TOXENV="py"
                    }
                    when{
                        equals expected: true, actual: params.TEST_RUN_TOX
                    }
                    steps {
                        sh "tox --workdir .tox -vv"
//                         script{
//                             try{
//                                 bat "tox --parallel=auto --parallel-live --workdir ${WORKSPACE}\\.tox -vv"
//                             } catch (exc) {
//                                 bat "tox --parallel=auto --parallel-live --workdir ${WORKSPACE}\\.tox --recreate -vv"
//                             }
//                         }
                    }
                }
                stage("MyPy"){
                    agent {
                        dockerfile {
                            filename 'ci/docker/python/linux/Dockerfile'
                            label 'linux && docker'
                        }
                    }
                    steps{
                        catchError(buildResult: "SUCCESS", message: 'MyPy found issues', stageResult: "UNSTABLE") {
                            sh(label: "Running MyPy",
                               script: """mkdir -p logs
                                          mypy -p hathi_validate --html-report reports/mypy_html > logs/mypy.log
                                          """
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
                stage("Documentation"){
                    agent {
                        dockerfile {
                            filename 'ci/docker/python/linux/Dockerfile'
                            label 'linux && docker'
                        }
                    }
                    steps{
                        sh "python -m sphinx -b doctest docs/source build/docs -d build/docs/doctrees -v"
                    }

                }
            }
        }
        stage("Packaging") {
            stages{
                stage("Building Python Distribution Packages"){
                    agent {
                        dockerfile {
                            filename 'ci/docker/python/linux/Dockerfile'
                            label 'linux && docker'
                        }
                    }
                    steps{
                        sh "python setup.py sdist --format zip -d dist bdist_wheel -d dist"

                    }
                    post{
                        always{
                            stash includes: 'dist/*.whl', name: "wheel"
                            stash includes: 'dist/*.zip', name: "sdist"
                        }
                        cleanup{
                            cleanWs notFailBuild: true
                        }
                    }
                }
                stage("Testing Packages"){
                    matrix{
                        axes {
                            axis {
                                name 'PYTHON_VERSION'
                                values(
                                    '3.6',
                                    '3.7',
                                    '3.8'
                                )
                            }
                            axis {
                                name 'PLATFORM'
                                values(
                                    "windows",
                                    "linux"
                                )
                            }
                            axis {
                                name 'FORMAT'
                                values(
                                    "sdist",
                                    "wheel"
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
                        stages{
                            stage("Testing Packages"){
                                agent {
                                    dockerfile {
                                        filename "${CONFIGURATIONS[PYTHON_VERSION].os[PLATFORM].agents.test[FORMAT].dockerfile.filename}"
                                        label "${CONFIGURATIONS[PYTHON_VERSION].os[PLATFORM].agents.test[FORMAT].dockerfile.label}"
                                        additionalBuildArgs "${CONFIGURATIONS[PYTHON_VERSION].os[PLATFORM].agents.test[FORMAT].dockerfile.additionalBuildArgs}"
                                     }
                                }
                                steps{
                                    script{
                                        if (FORMAT == "wheel"){
                                            unstash "wheel"
                                        }
                                        else{
                                            unstash "sdist"
                                        }
                                        findFiles( glob: "dist/**/${CONFIGURATIONS[PYTHON_VERSION].os[PLATFORM].pkgRegex[FORMAT]}").each{
                                            if(isUnix()){
                                                sh(
                                                    label: "Testing ${it}",
                                                    script: "tox --installpkg=${it.path} -e py"
                                                    )
                                            } else {
                                                bat(
                                                    label: "Testing ${it}",
                                                    script: "tox --installpkg=${it.path} -e py"
                                                )
                                            }
                                        }
                                    }
                                }
                                post{
                                    cleanup{
                                        cleanWs(
                                            notFailBuild: true,
                                            deleteDirs: true,
                                            patterns: [
                                                    [pattern: 'dist', type: 'INCLUDE'],
                                                    [pattern: 'build', type: 'INCLUDE'],
                                                    [pattern: '.tox', type: 'INCLUDE'],
                                                ]
                                        )
                                    }
                                }
                            }
                        }
                    }
                }
            }
            post{
                success{
                    archiveArtifacts artifacts: "dist/*.whl,dist/*.tar.gz,dist/*.zip", fingerprint: true
                }
            }
        }
        stage("Deploying to Devpi") {
            when {
                allOf{
                    equals expected: true, actual: params.DEPLOY_DEVPI
                    anyOf {
                        equals expected: "master", actual: env.BRANCH_NAME
                        equals expected: "dev", actual: env.BRANCH_NAME
                    }
                }
                beforeAgent true
            }
            options{
                timestamps()
            }
            environment{
                PATH = "${tool 'CPython-3.6'};${PATH}"
                PKG_NAME = get_package_name("DIST-INFO", "HathiValidate.dist-info/METADATA")
                PKG_VERSION = get_package_version("DIST-INFO", "HathiValidate.dist-info/METADATA")
                DEVPI = credentials("DS_devpi")
            }
            agent {
                label 'Windows&&Python3&&!aws'
            }
            stages{
                stage("Upload to DevPi staging") {
                    steps {
                        unstash "dist"
                        unstash "DOCUMENTATION"
                        bat "python -m venv venv"
                        bat "venv\\Scripts\\pip install devpi-client"
                        bat "venv\\Scripts\\devpi use https://devpi.library.illinois.edu && venv\\Scripts\\devpi login ${env.DEVPI_USR} --password ${env.DEVPI_PSW} && venv\\Scripts\\devpi use /${env.DEVPI_USR}/${env.BRANCH_NAME}_staging && venv\\Scripts\\devpi upload --from-dir dist"

                    }
                }
                stage("Test DevPi packages") {

                    parallel {
                        stage("Source Distribution: .zip") {
                            agent {
                                node {
                                    label "Windows && Python3"
                                }
                            }
                            options {
                                skipDefaultCheckout(true)
                            }
                            environment {
                                PATH = "${WORKSPACE}\\venv\\Scripts\\;${tool 'CPython-3.6'};${tool 'CPython-3.7'};$PATH"
                            }
                            stages{
                                stage("Building DevPi Testing venv for .zip package"){
                                    steps{
                                        lock("system_python_${NODE_NAME}"){
                                            bat "python -m venv venv"
                                        }
                                        bat "venv\\Scripts\\python.exe -m pip install pip --upgrade && venv\\Scripts\\pip.exe install setuptools --upgrade && venv\\Scripts\\pip.exe install \"tox<3.7\" detox devpi-client"
                                    }
                                }
                                stage("Testing DevPi zip Package"){
                                    options{
                                        timeout(20)
                                    }
                                    steps {
                                        echo "Testing Source tar.gz package in devpi"

                                        devpiTest(
                                            devpiExecutable: "${powershell(script: '(Get-Command devpi).path', returnStdout: true).trim()}",
                                            url: "https://devpi.library.illinois.edu",
                                            index: "${env.BRANCH_NAME}_staging",
                                            pkgName: "${env.PKG_NAME}",
                                            pkgVersion: "${env.PKG_VERSION}",
                                            pkgRegex: "zip",
                                            detox: false
                                        )
                                        echo "Finished testing Source Distribution: .zip"
                                    }

                                }
                            }

                            post {
                                cleanup{
                                        cleanWs notFailBuild: true
                                    }
                            }

                        }
                        stage("Built Distribution: .whl") {
                            agent {
                                node {
                                    label "Windows && Python3"
                                }
                            }
                            environment {
                                PATH = "${tool 'CPython-3.6'};${tool 'CPython-3.6'}\\Scripts;${tool 'CPython-3.7'};$PATH"
                            }
                            options {
                                skipDefaultCheckout(true)
                            }
                            stages{
                                stage("Creating venv to Test Whl"){
                                    steps {
                                        lock("system_python_${NODE_NAME}"){
                                            bat "if not exist venv\\36 mkdir venv\\36"
                                            bat "\"${tool 'CPython-3.6'}\\python.exe\" -m venv venv\\36"
                                            bat "if not exist venv\\37 mkdir venv\\37"
                                            bat "\"${tool 'CPython-3.7'}\\python.exe\" -m venv venv\\37"
                                        }
                                        bat "venv\\36\\Scripts\\python.exe -m pip install pip --upgrade && venv\\36\\Scripts\\pip.exe install setuptools --upgrade && venv\\36\\Scripts\\pip.exe install \"tox<3.7\" devpi-client"
                                    }

                                }
                                stage("Testing DevPi .whl Package"){
                                    options{
                                        timeout(20)
                                    }
                                    environment{
                                       PATH = "${WORKSPACE}\\venv\\36\\Scripts;${tool 'CPython-3.6'};${tool 'CPython-3.6'}\\Scripts;${tool 'CPython-3.7'};$PATH"
                                    }
                                    steps {
                                        echo "Testing Whl package in devpi"
                                        devpiTest(
//                                                devpiExecutable: "venv\\36\\Scripts\\devpi.exe",
                                            devpiExecutable: "${powershell(script: '(Get-Command devpi).path', returnStdout: true).trim()}",
                                            url: "https://devpi.library.illinois.edu",
                                            index: "${env.BRANCH_NAME}_staging",
                                            pkgName: "${env.PKG_NAME}",
                                            pkgVersion: "${env.PKG_VERSION}",
                                            pkgRegex: "whl",
                                            detox: false
                                            )

                                        echo "Finished testing Built Distribution: .whl"
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
                            branch "master"
                        }
                    }
                    steps {
                        script {
                            input "Release ${env.PKG_NAME} ${env.PKG_VERSION} to DevPi Production?"
                            withCredentials([usernamePassword(credentialsId: 'DS_devpi', usernameVariable: 'DEVPI_USERNAME', passwordVariable: 'DEVPI_PASSWORD')]) {
                                bat "venv\\Scripts\\devpi.exe login ${DEVPI_USERNAME} --password ${DEVPI_PASSWORD}"
                                bat "venv\\Scripts\\devpi.exe use /${DEVPI_USERNAME}/${env.BRANCH_NAME}_staging"
                                bat "venv\\Scripts\\devpi.exe push ${env.PKG_NAME}==${env.PKG_VERSION} production/release"
                            }
                        }
                    }
                }

            }
            post {
                success {
                    echo "it Worked. Pushing file to ${env.BRANCH_NAME} index"
                    script {
                        withCredentials([usernamePassword(credentialsId: 'DS_devpi', usernameVariable: 'DEVPI_USERNAME', passwordVariable: 'DEVPI_PASSWORD')]) {
                            bat "venv\\Scripts\\devpi.exe login ${DEVPI_USERNAME} --password ${DEVPI_PASSWORD}"
                            bat "venv\\Scripts\\devpi.exe use /${DEVPI_USERNAME}/${env.BRANCH_NAME}_staging"
                            bat "venv\\Scripts\\devpi.exe push ${env.PKG_NAME}==${env.PKG_VERSION} ${DEVPI_USERNAME}/${env.BRANCH_NAME}"
                        }
                    }
                }
                cleanup{
                    remove_from_devpi("venv\\Scripts\\devpi.exe", "${env.PKG_NAME}", "${env.PKG_VERSION}", "/${env.DEVPI_USR}/${env.BRANCH_NAME}_staging", "${env.DEVPI_USR}", "${env.DEVPI_PSW}")
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
    // post {
    //     cleanup{

    //          cleanWs(
    //             deleteDirs: true,
    //             patterns: [
    //                 [pattern: 'dist', type: 'INCLUDE'],
    //                 [pattern: 'reports', type: 'INCLUDE'],
    //                 [pattern: 'logs', type: 'INCLUDE'],
    //                 [pattern: 'certs', type: 'INCLUDE'],
    //                 [pattern: '*tmp', type: 'INCLUDE'],
    //                 [pattern: "source", type: 'INCLUDE'],
    //                 [pattern: "source/.git", type: 'EXCLUDE'],
    //                 [pattern: ".tox", type: 'INCLUDE'],
    //                 [pattern: "build", type: 'INCLUDE'],
    //                 [pattern: ".pytest_cache", type: 'INCLUDE']
    //                 ]
    //          )
    //     }
    // }
}
