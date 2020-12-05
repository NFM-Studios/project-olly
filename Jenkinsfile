pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh '''#!/bin/bash
                docker build -t nfmstudios/project-olly:master .
                docker network create -d bridge project-olly-net
                docker run -d --network=project-olly-net -e "POSTGRES_PASSWORD=secret_password" -e "POSTGRES_USER=olly" --name project-olly-db postgres:12
                sleep 30
                '''
            }
        }
        stage('Test') {
            steps {
                sh '''#!/bin/bash
                docker run --network=project-olly-net --env-file .env.example --name project-olly nfmstudios/project-olly:master python3 manage.py test 
                '''
            }
        }
    }
    post {
        always {
            script {
                def msg = "**Status:** " + currentBuild.currentResult.toLowerCase() + "\n"
                msg += "**Branch:** ${branch}\n"
                msg += "**Changes:** \n"
                if (!currentBuild.changeSets.isEmpty()) {
                    currentBuild.changeSets.first().getLogs().each {
                    msg += "- `" + it.getCommitId().substring(0, 8) + "` *" + it.getComment().substring(0, it.getComment().length()-1) + "*\n"
                    }
                } else {
                    msg += "no changes for this run\n"
                }
                if (msg.length() > 1024) msg.take(msg.length() - 1024)
            }
            withCredentials([string(credentialsId: 'Webook_URL', variable: 'WEBHOOK_URL')]) {
                discordSend description: "${msg}", link: env.BUILD_URL, result: currentBuild.currentResult, title: "Project Olly:${branch} #${BUILD_NUMBER}", webhookURL: env.WEBHOOK_URL
                }
            }
        cleanup {
            sh '''#!/bin/bash
            docker rm -f project-olly 2> /dev/null
            docker rm -f project-olly-db 2> /dev/null
            docker network rm project-olly-net 2> /dev/null
            docker rmi nfmstudios/project-olly:master 2> /dev/null 
            '''
        }
    }
}
