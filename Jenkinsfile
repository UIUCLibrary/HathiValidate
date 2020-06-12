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
                            dockerfile: [
                                filename: 'ci/docker/python/windows/Dockerfile',
                                label: 'Windows&&Docker',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.6-windowsservercore'
                            ]
                        ],
                        devpi: [
                            dockerfile: [
                                filename: 'ci/docker/python/windows/Dockerfile',
                                label: 'Windows && Docker',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.6-windowsservercore'
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
                            dockerfile: [
                                filename: 'ci/docker/python/linux/Dockerfile',
                                label: 'linux&&docker',
                                additionalBuildArgs: '--build-arg PYTHON_VERSION=3.6 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                            ]
                        ],
                        devpi: [
                            dockerfile: [
                                filename: 'ci/docker/python/linux/Dockerfile',
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
                                filename: 'ci/docker/python/windows/Dockerfile',
                                label: 'Windows&&Docker',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.7'
                            ]
                        ],
                        test: [
                            dockerfile: [
                                filename: 'ci/docker/python/windows/Dockerfile',
                                label: 'Windows&&Docker',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.7'
                            ]
                        ],
                        devpi: [
                            dockerfile: [
                                filename: 'ci/docker/python/windows/Dockerfile',
                                label: 'Windows && Docker',
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
                                filename: 'ci/docker/python/linux/Dockerfile',
                                label: 'linux&&docker',
                                additionalBuildArgs: '--build-arg PYTHON_VERSION=3.7 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                            ]
                        ],
                        test: [
                            dockerfile: [
                                filename: 'ci/docker/python/linux/Dockerfile',
                                label: 'linux&&docker',
                                additionalBuildArgs: '--build-arg PYTHON_VERSION=3.7 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                            ]
                        ],
                        devpi: [
                            dockerfile: [
                                filename: 'ci/docker/python/linux/Dockerfile',
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
                                filename: 'ci/docker/python/windows/Dockerfile',
                                label: 'Windows&&Docker',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.8'
                            ]
                        ],
                        test: [
                            dockerfile: [
                                filename: 'ci/docker/python/windows/Dockerfile',
                                label: 'Windows && Docker',
                                additionalBuildArgs: '--build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.8'
                            ]
                        ],
                        devpi: [
                            dockerfile: [
                                filename: 'ci/docker/python/windows/Dockerfile',
                                label: 'Windows && Docker',
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
                                filename: 'ci/docker/python/linux/Dockerfile',
                                label: 'linux&&docker',
                                additionalBuildArgs: '--build-arg PYTHON_VERSION=3.8 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                            ]
                        ],
                        test: [
                            dockerfile: [
                                filename: 'ci/docker/python/linux/Dockerfile',
                                label: 'linux&&docker',
                                additionalBuildArgs: '--build-arg PYTHON_VERSION=3.8 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                            ]
                        ],
                        devpi: [
                            dockerfile: [
                                filename: 'ci/docker/python/linux/Dockerfile',
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
        buildDiscarder logRotator(artifactDaysToKeepStr: '10', artifactNumToKeepStr: '10')
    }
    triggers {
        parameterizedCron '@daily % DEPLOY_DEVPI=true; TEST_RUN_TOX=true'
    }
    parameters {
        string(name: "PROJECT_NAME", defaultValue: "Hathi Validate", description: "Name given to the project")
        booleanParam(name: "TEST_RUN_TOX", defaultValue: false, description: "Run Tox Tests")
        booleanParam(name: "DEPLOY_DEVPI", defaultValue: false, description: "Deploy to devpi on http://devpy.library.illinois.edu/DS_Jenkins/${env.BRANCH_NAME}")
        booleanParam(name: "DEPLOY_DEVPI_PRODUCTION", defaultValue: false, description: "Deploy to https://devpi.library.illinois.edu/production/release")
        booleanParam(name: "DEPLOY_ADD_TAG", defaultValue: false, description: "Tag commit to current version")
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
                            script{
                                def DOC_ZIP_FILENAME = "${env.PKG_NAME}-${env.PKG_VERSION}.doc.zip"
                                zip archive: true, dir: "build/docs/html", glob: '', zipFile: "dist/${DOC_ZIP_FILENAME}"
                                stash includes: "build/docs/**,dist/${DOC_ZIP_FILENAME}", name: "DOCUMENTATION"
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
                stage("Doctest"){
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
                        success{
                            archiveArtifacts artifacts: "dist/*.whl,dist/*.tar.gz,dist/*.zip", fingerprint: true
                        }
                        cleanup{
                            cleanWs notFailBuild: true
                        }
                    }
                }
                stage("Testing Packages"){
                    options{
                        timestamps()
                    }
                    matrix{
                        axes {
                            axis {
                                name 'PYTHON_VERSION'
                                values(
                                    '3.8',
                                    '3.7',
                                    '3.6'
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
                                    "wheel",
                                    "sdist"
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
                                        filename "${CONFIGURATIONS[PYTHON_VERSION].os[PLATFORM].agents.test.dockerfile.filename}"
                                        label "${CONFIGURATIONS[PYTHON_VERSION].os[PLATFORM].agents.test.dockerfile.label}"
                                        additionalBuildArgs "${CONFIGURATIONS[PYTHON_VERSION].os[PLATFORM].agents.test.dockerfile.additionalBuildArgs}"
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
                                                    script: "tox --installpkg=${it.path} -e py -v"
                                                    )
                                            } else {
                                                bat(
                                                    label: "Testing ${it}",
                                                    script: "tox --installpkg=${it.path} -e py -v"
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
        }
        stage("Deploy to Devpi"){
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
                            filename 'ci/docker/python/linux/Dockerfile'
                            label 'linux && docker'
                            additionalBuildArgs '--build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                          }
                    }
                    steps {
                        timeout(5){
                            unstash "wheel"
                            unstash "sdist"
                            unstash "DOCUMENTATION"
                            sh(
                                label: "Connecting to DevPi Server",
                                script: 'devpi use https://devpi.library.illinois.edu --clientdir ${WORKSPACE}/devpi && devpi login $DEVPI_USR --password $DEVPI_PSW --clientdir ${WORKSPACE}/devpi'
                            )
                            sh(
                                label: "Uploading to DevPi Staging",
                                script: """devpi use /${env.DEVPI_USR}/${env.BRANCH_NAME}_staging --clientdir ${WORKSPACE}/devpi
    devpi upload --from-dir dist --clientdir ${WORKSPACE}/devpi"""
                            )
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
                                    unstash "DIST-INFO"
                                    script{
                                        def props = readProperties interpolate: true, file: "HathiValidate.dist-info/METADATA"

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
                            branch "master"
                        }
                        beforeAgent true
                    }
                    agent {
                        dockerfile {
                            filename 'ci/docker/python/linux/Dockerfile'
                            label 'linux&&docker'
                            additionalBuildArgs '--build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                        }
                    }
                    steps {
                        script {
                            unstash "DIST-INFO"
                            def props = readProperties interpolate: true, file: 'HathiValidate.dist-info/METADATA'
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
                            docker.build("hathivalidate:devpi.${env.BUILD_ID}",'-f ./ci/docker/python/linux/Dockerfile --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) .').inside{
                                unstash "DIST-INFO"
                                def props = readProperties interpolate: true, file: 'HathiValidate.dist-info/METADATA'
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
                            docker.build("hathivalidate:devpi.${env.BUILD_ID}",'-f ./ci/docker/python/linux/Dockerfile --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) .').inside{
                                unstash "DIST-INFO"
                                def props = readProperties interpolate: true, file: 'HathiValidate.dist-info/METADATA'
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
                stage("Tagging git Commit"){
                    agent {
                        dockerfile {
                            filename 'ci/docker/python/linux/Dockerfile'
                            label 'linux && docker'
                            additionalBuildArgs '--build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                        }
                    }
                    when{
                        allOf{
                            equals expected: true, actual: params.DEPLOY_ADD_TAG
                        }
                        beforeAgent true
                        beforeInput true
                    }
                    options{
                        timeout(time: 1, unit: 'DAYS')
                        retry(3)
                    }
                    input {
                          message 'Add a version tag to git commit?'
                          parameters {
                                credentials credentialType: 'com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl', defaultValue: 'github.com', description: '', name: 'gitCreds', required: true
                          }
                    }
                    steps{
                        unstash "DIST-INFO"
                        script{
                            def props = readProperties interpolate: true, file: "HathiValidate.dist-info/METADATA"
                            def commitTag = input message: 'git commit', parameters: [string(defaultValue: "v${props.Version}", description: 'Version to use a a git tag', name: 'Tag', trim: false)]
                            withCredentials([usernamePassword(credentialsId: gitCreds, passwordVariable: 'password', usernameVariable: 'username')]) {
                                sh(label: "Tagging ${commitTag}",
                                   script: """git config --local credential.helper "!f() { echo username=\\$username; echo password=\\$password; }; f"
                                              git tag -a ${commitTag} -m 'Tagged by Jenkins'
                                              git push origin --tags
                                   """
                                )
                            }
                        }
                    }
                    post{
                        cleanup{
                            deleteDir()
                        }
                    }
                }
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
