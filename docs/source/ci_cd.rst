CI/CD
=====

Workflows can also be set up and run on an automation server to enable continuous integration/continuous delivery (CI/CD).

This page will guide you through the process of setting up an CI/CD automation server (Jenkins) and hosting your example workflow there.


#. Install the Jenkins-server Docker image

   In this tutorial, we will use the `jenkin-server <https://hub.docker.com/repository/docker/clin864/jenkins-server>`_ Docker image to set up our Jenkins server.
   The complete installation guild of the Jenkins-server image can be found in `here <https://lin810116.github.io/jenkins-server/installation.html>`_

#. Setting up your workflow in Jenkins

   See `this section <https://lin810116.github.io/jenkins-server/setting_up_automation_pipeline.html#>`_ in the Jenkins-server documentation to create a Jenkins pipeline for your workflow.
   The `Setting up CI/CD pipeline <https://lin810116.github.io/jenkins-server/setting_up_automation_pipeline.html#setting-up-ci-cd-pipeline>`_ sub-section is where you should provide your own Jenkins pipeline script for setting up your workflow.
   Below is an example of the pipeline script you can refer to.

   .. code-block::

      pipeline {
        agent any

        environment {
            REMOTE_URL = 'git@github.com:LIN810116/workflow-manager.git'
            CREDENTIAL_ID = 'workflow-manager-clin864'
            BRANCH = 'main'
            USER_NAME = 'lin810116'
            USER_EMAIL = 'lin810116@gmail.com'
            TEST_MODULE = 'tests/'
            SOURCE_DIR = './docs/source'
            BUILD_DIR = './docs/build'
            PYENV_VERSION = '3.6.15'
            PYTHONPATH='/var/jenkins_home/workspace/workflow-manager'
            WORKSPACE = "workspace"
        }

        stages {
            stage('Environment Setup') {
                steps{
                    sh 'printenv'

                    echo "Cloning GitHub repository..."
                    git branch: "${BRANCH}", credentialsId: "${CREDENTIAL_ID}", url: "${REMOTE_URL}"
                    echo "Creating virtual environment"
                    sh '''
                        python --version
                        python -m venv venv
                    '''

                    // set up mongodb
                    sh'''
                        wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | apt-key add -
                        echo "deb http://repo.mongodb.org/apt/debian buster/mongodb-org/4.4 main" | tee /etc/apt/sources.list.d/mongodb-org-4.4.list
                        apt-get update
                        apt-get install -y mongodb-org
                    '''
                    withEnv(['JENKINS_NODE_COOKIE =dontkill']) {
                        // Run in background
                        sh '''
                            nohup mongod --port 27017 --dbpath /var/jenkins_home/workspace/workflow-manager/data/db --bind_ip 'localhost' &
                        '''
                    }

                    echo "Installing dependencies..."
                    sh '''
                        . venv/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                    '''

                    echo "Creating worspace"
                    sh '''
                    mkdir -p ${WORKSPACE}
                    '''

                }
            }

            stage ('Import Scans'){
                steps {
                    sh '''
                        . venv/bin/activate
                        python examples/scripts/pretend_import.py --workflow False --source examples/data/pretend_data.txt --dest ${WORKSPACE}
                    '''
                }
            }

            stage ('Segment'){
                steps {
                    sh '''
                        . venv/bin/activate
                        python examples/scripts/pretend_segment.py --workflow False --source ${WORKSPACE}/pretend_data.txt --dest ${WORKSPACE}/pointcloud.txt
                    '''
                }
            }

            stage ('Fit mesh'){
                steps {
                    sh '''
                        . venv/bin/activate
                        python examples/scripts/pretend_fit.py --workflow False --source ${WORKSPACE}/pointcloud.txt --dest ${WORKSPACE}/mesh.txt
                    '''
                }
            }

            stage ('Mechanics'){
                steps {
                    sh '''
                        . venv/bin/activate
                        python examples/scripts/pretend_mechanics1.py --workflow False --source ${WORKSPACE}/mesh.txt --dest ${WORKSPACE}/solution1.txt
                    '''
                }
            }

            stage ('Send results'){
                steps {
                    sh '''
                        . venv/bin/activate
                        mkdir -p results
                        python examples/scripts/pretend_send.py --workflow False --source ${WORKSPACE} --dest results

                    '''
                }
            }

            // stage ('Test'){
            //     steps {
            //         echo "Running tests"
            //         // sh '''
            //         //     . venv/bin/activate
            //         //     pytest ./tests/test_example_workflow.py
            //         //     pytest ./tests/test_functionalities.py
            //         // '''
            //         // sh '''
            //         //     . venv/bin/activate
            //         //     pytest --junit-xml=report.xml -o junit_family=xunit2 ./tests/test_example_workflow.py
            //         // '''
            //         sh '''
            //             . venv/bin/activate
            //             pytest --junit-xml=report.xml -o junit_family=xunit2 ${TEST_MODULE}
            //         '''
            //     }
            // }



            // stage('Build docs') {
            //     steps {
            //         echo "Building"
            //         echo "${WORKSPACE}"
            //         sh "${WORKSPACE}/venv/bin/sphinx-build -b html ${SOURCE_DIR} ${BUILD_DIR}"
            //     }
            // }


            // stage("Deploy Docs") {
            //     steps {
            //         echo "Deploying to GitHub pages"
            //         sh '''
            //             git config --global user.email ${USER_EMAIL}
            //             git config --global user.name ${USER_NAME}
            //         '''

            //         sh 'npm install -g --silent gh-pages@2.1.1'
            //         sh 'touch ${BUILD_DIR}/.nojekyll'
            //         sshagent(credentials: ["${CREDENTIAL_ID}"]) {
            //             sh '''
            //                 gh-pages --dotfiles --message '[skip ci] Updates' --dist ${BUILD_DIR}
            //             '''
            //         }
            //     }
            // }

        }

        // post {
        //     always {
        //         junit 'report.xml'
        //     }
        // }
    }
