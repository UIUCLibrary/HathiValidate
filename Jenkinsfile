@Library("ds-utils")
// Uses https://github.com/UIUCLibrary/Jenkins_utils
import org.ds.*

pipeline {
    agent {
        label "Windows&&DevPi"
    }
    options {
        disableConcurrentBuilds()  //each branch has 1 job running at a time
    }

    environment {
        mypy_args = "--junit-xml=mypy.xml"
        //pytest_args = "--junitxml=reports/junit-{env:OS:UNKNOWN_OS}-{envname}.xml --junit-prefix={env:OS:UNKNOWN_OS}  --basetemp={envtmpdir}"
    }
    parameters {
        string(name: "PROJECT_NAME", defaultValue: "Hathi Validate", description: "Name given to the project")
        booleanParam(name: "UNIT_TESTS", defaultValue: true, description: "Run Automated Unit Tests")
        booleanParam(name: "ADDITIONAL_TESTS", defaultValue: true, description: "Run additional tests")
        // booleanParam(name: "PACKAGE", defaultValue: true, description: "Create a Packages")
        // booleanParam(name: "DEPLOY_SCCM", defaultValue: false, description: "Deploy SCCM")
        booleanParam(name: "DEPLOY_DEVPI", defaultValue: true, description: "Deploy to devpi on http://devpy.library.illinois.edu/DS_Jenkins/${env.BRANCH_NAME}")
        choice(choices: 'None\nRelease_to_devpi_only\nRelease_to_devpi_and_sccm\n', description: "Release the build to production. Only available in the Master branch", name: 'RELEASE')
        booleanParam(name: "UPDATE_DOCS", defaultValue: false, description: "Update the documentation")
        string(name: 'URL_SUBFOLDER', defaultValue: "hathi_validate", description: 'The directory that the docs should be saved under')
    }
    stages {
        stage("Cloning Source") {

            steps {
                deleteDir()
                checkout scm
                stash includes: '**', name: "Source", useDefaultExcludes: false
                stash includes: 'deployment.yml', name: "Deployment"

            }

        }
        stage("Unit tests") {
            when {
                expression { params.UNIT_TESTS == true }
            }
            steps {
                parallel(
                    "PyTest": {
                        node(label: "Windows") {
                            checkout scm
                            // bat "${tool 'Python3.6.3_Win64'} -m tox -e py36"
                            bat "${tool 'Python3.6.3_Win64'} -m tox -e pytest -- --junitxml=reports/junit-${env.NODE_NAME}-pytest.xml --junit-prefix=${env.NODE_NAME}-pytest" //  --basetemp={envtmpdir}" 
                            junit "reports/junit-${env.NODE_NAME}-pytest.xml"
                         }
                    },
                    "Behave": {
                        node(label: "Windows") {
                            checkout scm
                            bat "${tool 'Python3.6.3_Win64'} -m tox -e behave --  --junit --junit-directory reports" 
                            junit "reports/*.xml"
                        }
                    }
                )
                
            }
        }
        // stage("Unit tests") {
        //     when {
        //         expression { params.UNIT_TESTS == true }
        //     }
        //     steps {
        //         node(label: "Windows") {
        //             checkout scm
        //             // bat "${tool 'Python3.6.3_Win64'} -m tox -e py36"
        //             bat "${tool 'Python3.6.3_Win64'} -m tox -e py36 -- --junitxml=reports/junit-${env.NODE_NAME}-pytest.xml --junit-prefix=${env.NODE_NAME}-pytest" //  --basetemp={envtmpdir}" 
        //             junit "reports/junit-${env.NODE_NAME}-pytest.xml"
        //             }
                
        //     }
        // }
        // // stage("Unit tests") {
        // //     when {
        // //         expression { params.UNIT_TESTS == true }
        // //     }
        // //     steps {
        // //         parallel(
        // //                 "Windows": {
        // //                     script {
        // //                         def runner = new Tox(this)
        // //                         runner.env = "pytest"
        // //                         runner.windows = true
        // //                         runner.stash = "Source"
        // //                         runner.label = "Windows"
        // //                         runner.post = {
        // //                             junit 'reports/junit-*.xml'
        // //                         }
        // //                         runner.run()
        // //                     }
        // //                 },
        // //                 // "Linux": {
        // //                 //     script {
        // //                 //         def runner = new Tox(this)
        // //                 //         runner.env = "pytest"
        // //                 //         runner.windows = false
        // //                 //         runner.stash = "Source"
        // //                 //         runner.label = "!Windows"
        // //                 //         runner.post = {
        // //                 //             junit 'reports/junit-*.xml'
        // //                 //         }
        // //                 //         runner.run()
        // //                 //     }
        // //                 // }
        // //         )
        // //     }
        // // }
        // // stage("Additional tests") {
        // //     when {
        // //         expression { params.ADDITIONAL_TESTS == true }
        // //     }

        // //     steps {
        // //         parallel(
        // //                 "Documentation": {
        // //                     script {
        // //                         def runner = new Tox(this)
        // //                         runner.env = "docs"
        // //                         runner.windows = true
        // //                         runner.stash = "Source"
        // //                         runner.label = "Windows"
        // //                         runner.post = {
        // //                             dir('.tox/dist/html/') {
        // //                                 stash includes: '**', name: "HTML Documentation", useDefaultExcludes: false
        // //                             }
        // //                         }
        // //                         runner.run()

        // //                     }
        // //                 },
        // //                 "MyPy": {
        // //                     node(label: "Windows") {
        // //                         checkout scm
        // //                         bat "make test-mypy --html-report reports/mypy_report --junit-xml reports/mypy.xml"
        // //                         junit 'reports/mypy.xml'
        // //                     }
        // //                   }
        // //                 // "MyPy": {
        // //                 //     script {
        // //                 //         def runner = new Tox(this)
        // //                 //         runner.env = "mypy"
        // //                 //         runner.windows = true
        // //                 //         runner.stash = "Source"
        // //                 //         runner.label = "Windows"
        // //                 //         runner.post = {
        // //                 //             junit 'mypy.xml'
        // //                 //         }
        // //                 //         runner.run()

        // //                 //     }
        // //                 // }
        // //         )
        // //     }

        // // }
        stage("Additional tests") {
            when {
                expression { params.ADDITIONAL_TESTS == true }
            }

            steps {
                parallel(
                        "Documentation": {
                            node(label: "Windows") {
                                checkout scm
                                bat "${tool 'Python3.6.3_Win64'} -m tox -e docs"
                                dir('.tox/dist') {
                                    zip archive: true, dir: 'html', glob: '', zipFile: 'sphinx_html_docs.zip'
                                    dir("html"){
                                        stash includes: '**', name: "HTML Documentation"
                                    }
                                }
                            }
                          
                        },
                        "MyPy": {
                            node(label: "Windows") {
                                checkout scm
                                bat "make test-mypy --html-report reports/mypy_report --junit-xml reports/mypy.xml"
                                junit 'reports/mypy.xml'
                            }
                          }
                )
            }
        }
        // stage("Packaging") {
        //     when {
        //         expression { params.PACKAGE == true }
        //     }
        //     steps {
        //         parallel(
        //                 "Windows Wheel": {
        //                     node(label: "Windows") {
        //                         deleteDir()
        //                         unstash "Source"
        //                         bat "${env.PYTHON3} setup.py bdist_wheel --universal"
        //                         archiveArtifacts artifacts: "dist/**", fingerprint: true
        //                     }
        //                 },
        //                 "Windows CX_Freeze MSI": {
        //                     node(label: "Windows") {
        //                         deleteDir()
        //                         unstash "Source"
        //                         bat """ ${env.PYTHON3} -m venv .env
        //                   call .env/Scripts/activate.bat
        //                   pip install -r requirements.txt
        //                   python cx_setup.py bdist_msi --add-to-path=true
        //                   """

        //                         dir("dist") {
        //                             stash includes: "*.msi", name: "msi"
        //                         }

        //                     }
        //                     node(label: "Windows") {
        //                         deleteDir()
        //                         git url: 'https://github.com/UIUCLibrary/ValidateMSI.git'
        //                         unstash "msi"

        //                         bat """
        //                   ${env.PYTHON3} -m venv .env
        //                   call .env/Scripts/activate.bat
        //                   pip install --upgrade pip
        //                   pip install setuptools --upgrade
        //                   pip install -r requirements.txt
        //                   python setup.py install
    
        //                   echo Validating msi file(s)
        //                   FOR /f "delims=" %%A IN ('dir /b /s *.msi') DO (
        //                     python validate_msi.py ^"%%A^" frozen.yml
        //                     if not %errorlevel%==0 (
        //                       echo errorlevel=%errorlevel%
        //                       exit /b %errorlevel%
        //                       )
        //                     )
        //                   """
        //                         archiveArtifacts artifacts: "*.msi", fingerprint: true
        //                     }
        //                 },
        //                 "Source Release": {
        //                     createSourceRelease(env.PYTHON3, "Source")
        //                 }
        //         )
        //     }
        // }
        stage("Packaging") {
            when {
                expression { params.DEPLOY_DEVPI == true || params.RELEASE != "None"}
            }

            steps {
                parallel(
                        "Source and Wheel formats": {
                            bat "call make.bat"
                            // bat """${tool 'Python3.6.3_Win64'} -m venv venv
                            //         call venv\\Scripts\\activate.bat
                            //         pip install -r requirements.txt
                            //         pip install -r requirements-dev.txt
                            //         python setup.py sdist bdist_wheel
                            //         """
                        },
                        "Windows CX_Freeze MSI": {
                            node(label: "Windows") {
                                deleteDir()
                                checkout scm
                                bat "${tool 'Python3.6.3_Win64'} -m venv venv"
                                bat "make freeze"
                                dir("dist") {
                                    stash includes: "*.msi", name: "msi"
                                }

                            }
                            node(label: "Windows") {
                                deleteDir()
                                git url: 'https://github.com/UIUCLibrary/ValidateMSI.git'
                                unstash "msi"
                                bat "call validate.bat -i"
                                
                            }
                        },
                )
            }
            post {
              success {
                  dir("dist"){
                      unstash "msi"
                      archiveArtifacts artifacts: "*.whl", fingerprint: true
                      archiveArtifacts artifacts: "*.tar.gz", fingerprint: true
                      archiveArtifacts artifacts: "*.msi", fingerprint: true
                }
              }
            }
            
        }
        // stage("Deploy - Staging") {
        //     agent any
        //     when {
        //         expression { params.DEPLOY_SCCM == true && params.PACKAGE == true }
        //     }
        //     steps {
        //         deployStash("msi", "${env.SCCM_STAGING_FOLDER}/${params.PROJECT_NAME}/")
        //         input("Deploy to production?")
        //     }
        // }

        // stage("Deploy - SCCM upload") {
        //     agent any
        //     when {
        //         expression { params.DEPLOY_SCCM == true && params.PACKAGE == true }
        //     }
        //     steps {
        //         deployStash("msi", "${env.SCCM_UPLOAD_FOLDER}")
        //     }
        //     post {
        //         success {
        //             script {
        //                 unstash "Source"
        //                 def deployment_request = requestDeploy this, "deployment.yml"
        //                 echo deployment_request
        //                 writeFile file: "deployment_request.txt", text: deployment_request
        //                 archiveArtifacts artifacts: "deployment_request.txt"
        //             }
        //         }
        //     }
        // }
        // stage("Deploying to Devpi") {
        //     agent {
        //         node {
        //             label 'Windows'
        //         }
        //     }
        //     when {
        //         expression { params.DEPLOY_DEVPI == true }
        //     }
        //     steps {
        //         deleteDir()
        //         unstash "Source"
        //         bat "devpi use http://devpy.library.illinois.edu"
        //         withCredentials([usernamePassword(credentialsId: 'DS_devpi', usernameVariable: 'DEVPI_USERNAME', passwordVariable: 'DEVPI_PASSWORD')]) {
        //             bat "devpi login ${DEVPI_USERNAME} --password ${DEVPI_PASSWORD}"
        //             bat "devpi use /${DEVPI_USERNAME}/${env.BRANCH_NAME}"
        //             script {
        //                 try{
        //                     bat "devpi upload --with-docs"

        //                 } catch (exc) {
        //                     echo "Unable to upload to devpi with docs. Trying without"
        //                     bat "devpi upload"
        //                 }
        //             }
        //             bat "devpi test HathiValidate"
        //         }
        //     }
        // }
        stage("Deploying to Devpi") {
            when {
                expression { params.DEPLOY_DEVPI == true && (env.BRANCH_NAME == "master" || env.BRANCH_NAME == "dev")}
            }
            steps {
                bat "${tool 'Python3.6.3_Win64'} -m devpi use http://devpy.library.illinois.edu"
                withCredentials([usernamePassword(credentialsId: 'DS_devpi', usernameVariable: 'DEVPI_USERNAME', passwordVariable: 'DEVPI_PASSWORD')]) {
                    bat "${tool 'Python3.6.3_Win64'} -m devpi login ${DEVPI_USERNAME} --password ${DEVPI_PASSWORD}"
                    bat "${tool 'Python3.6.3_Win64'} -m devpi use /${DEVPI_USERNAME}/${env.BRANCH_NAME}_staging"
                    script {
                        bat "${tool 'Python3.6.3_Win64'} -m devpi upload --from-dir dist"
                        try {
                            bat "${tool 'Python3.6.3_Win64'} -m devpi upload --only-docs"
                        } catch (exc) {
                            echo "Unable to upload to devpi with docs."
                        }
                    }
                }

            }
        }
        stage("Test Devpi packages") {
            when {
                expression { params.DEPLOY_DEVPI == true && (env.BRANCH_NAME == "master" || env.BRANCH_NAME == "dev")}
            }
            steps {
                parallel(
                        "Source": {
                            script {
                                def name = bat(returnStdout: true, script: "@${tool 'Python3.6.3_Win64'} setup.py --name").trim()
                                def version = bat(returnStdout: true, script: "@${tool 'Python3.6.3_Win64'} setup.py --version").trim()
                                node("Windows") {
                                    withCredentials([usernamePassword(credentialsId: 'DS_devpi', usernameVariable: 'DEVPI_USERNAME', passwordVariable: 'DEVPI_PASSWORD')]) {
                                        bat "${tool 'Python3.6.3_Win64'} -m devpi login ${DEVPI_USERNAME} --password ${DEVPI_PASSWORD}"
                                        bat "${tool 'Python3.6.3_Win64'} -m devpi use /${DEVPI_USERNAME}/${env.BRANCH_NAME}_staging"
                                        echo "Testing Source package in devpi"
                                        bat "${tool 'Python3.6.3_Win64'} -m devpi test --index http://devpy.library.illinois.edu/${DEVPI_USERNAME}/${env.BRANCH_NAME}_staging ${name} -s tar.gz"
                                    }
                                }

                            }
                        },
                        "Wheel": {
                            script {
                                def name = bat(returnStdout: true, script: "@${tool 'Python3.6.3_Win64'} setup.py --name").trim()
                                def version = bat(returnStdout: true, script: "@${tool 'Python3.6.3_Win64'} setup.py --version").trim()
                                node("Windows") {
                                    withCredentials([usernamePassword(credentialsId: 'DS_devpi', usernameVariable: 'DEVPI_USERNAME', passwordVariable: 'DEVPI_PASSWORD')]) {
                                        bat "${tool 'Python3.6.3_Win64'} -m devpi login ${DEVPI_USERNAME} --password ${DEVPI_PASSWORD}"
                                        bat "${tool 'Python3.6.3_Win64'} -m devpi use /${DEVPI_USERNAME}/${env.BRANCH_NAME}_staging"
                                        echo "Testing Whl package in devpi"
                                        bat " ${tool 'Python3.6.3_Win64'} -m devpi test --index http://devpy.library.illinois.edu/${DEVPI_USERNAME}/${env.BRANCH_NAME}_staging ${name} -s whl"
                                    }
                                }

                            }
                        }
                )

            }
            post {
                success {
                    echo "it Worked. Pushing file to ${env.BRANCH_NAME} index"
                    script {
                        def name = bat(returnStdout: true, script: "@${tool 'Python3.6.3_Win64'} setup.py --name").trim()
                        def version = bat(returnStdout: true, script: "@${tool 'Python3.6.3_Win64'} setup.py --version").trim()
                        withCredentials([usernamePassword(credentialsId: 'DS_devpi', usernameVariable: 'DEVPI_USERNAME', passwordVariable: 'DEVPI_PASSWORD')]) {
                            bat "${tool 'Python3.6.3_Win64'} -m devpi login ${DEVPI_USERNAME} --password ${DEVPI_PASSWORD}"
                            bat "${tool 'Python3.6.3_Win64'} -m devpi use /${DEVPI_USERNAME}/${env.BRANCH_NAME}_staging"
                            bat "${tool 'Python3.6.3_Win64'} -m devpi push ${name}==${version} ${DEVPI_USERNAME}/${env.BRANCH_NAME}"
                        }

                    }
                }
            }
        }
        stage("Release to DevPi production") {
            when {
                expression { params.RELEASE != "None" && env.BRANCH_NAME == "master" }
            }
            steps {
                script {
                    def name = bat(returnStdout: true, script: "@${tool 'Python3.6.3_Win64'} setup.py --name").trim()
                    def version = bat(returnStdout: true, script: "@${tool 'Python3.6.3_Win64'} setup.py --version").trim()
                    withCredentials([usernamePassword(credentialsId: 'DS_devpi', usernameVariable: 'DEVPI_USERNAME', passwordVariable: 'DEVPI_PASSWORD')]) {
                        bat "${tool 'Python3.6.3_Win64'} -m devpi login ${DEVPI_USERNAME} --password ${DEVPI_PASSWORD}"
                        bat "${tool 'Python3.6.3_Win64'} -m devpi use /${DEVPI_USERNAME}/${env.BRANCH_NAME}_staging"
                        bat "${tool 'Python3.6.3_Win64'} -m devpi push ${name}==${version} production/release"
                    }

                }
                node("Linux"){
                    updateOnlineDocs url_subdomain: params.URL_SUBFOLDER, stash_name: "HTML Documentation"
                }
            }
        }

        stage("Deploy to SCCM") {
            when {
                expression { params.RELEASE == "Release_to_devpi_and_sccm"}
            }

            steps {
                node("Linux"){
                    unstash "msi"
                    deployStash("msi", "${env.SCCM_STAGING_FOLDER}/${params.PROJECT_NAME}/")
                    input("Deploy to production?")
                    deployStash("msi", "${env.SCCM_UPLOAD_FOLDER}")
                }

            }
            post {
                success {
                    script{
                        def  deployment_request = requestDeploy this, "deployment.yml"
                        echo deployment_request
                        writeFile file: "deployment_request.txt", text: deployment_request
                        archiveArtifacts artifacts: "deployment_request.txt"
                    }
                }
            }
        }
        stage("Update online documentation") {
            agent any
            when {
                expression { params.UPDATE_DOCS == true }
            }

            steps {
                updateOnlineDocs url_subdomain: params.URL_SUBFOLDER, stash_name: "HTML Documentation"
            }
        }
    }
    post {
        always {
            script {
                def name = bat(returnStdout: true, script: "@${tool 'Python3.6.3_Win64'} setup.py --name").trim()
                def version = bat(returnStdout: true, script: "@${tool 'Python3.6.3_Win64'} setup.py --version").trim()
                withCredentials([usernamePassword(credentialsId: 'DS_devpi', usernameVariable: 'DEVPI_USERNAME', passwordVariable: 'DEVPI_PASSWORD')]) {
                    bat "${tool 'Python3.6.3_Win64'} -m devpi remove -y ${name}==${version}"
                }
            }
        }
        success {
            echo "Cleaning up workspace"
            deleteDir()
        }
    }
}
