def getSchemaFromGitea(branch, credentials,project_folder) {
	sh "rm -r -f "+project_folder
    withCredentials([string(credentialsId: credentials, variable: 'gitea_token')]) {
    	// some block 
        sh "git clone -c http.sslVerify=false -b " + "develop" + " https://" + gitea_token + ":x-oauth-basic@gitea.gpapdev.cnag.eu/gitea/platform/"+project_folder
        sh "cd "+project_folder+" && git fetch --all"
    
        try {
            sh "cd "+project_folder+" && git checkout -b " + branch
        }
        catch(Exception e1) {
            sh "cd "+project_folder+" && git checkout  " + branch
           println(e1);
  
        }       
        try {
            sh "cd "+project_folder+" && git pull origin " + branch 
        }
        catch(Exception e1) {
            println(e1);
        }    
        //sh "cp -r "+project_folder+"/formSchema/UIconfig.js ./treatabolome_server/config/."        
	}
}

def getConfigFromGitea(branch, credentials,project_folder) {              
	sh "rm -r -f "+project_folder
    withCredentials([string(credentialsId: credentials, variable: 'gitea_token')]) {
    	// some block
		sh "git clone -c http.sslVerify=false -b " + "develop" + " https://" + gitea_token + ":x-oauth-basic@gitea.gpapdev.cnag.eu/gitea/platform/"+project_folder
        sh "cd "+project_folder+" && git fetch --all"
		try {
			sh "cd "+project_folder+" && git checkout -b " + branch
		}
		catch(Exception e1) {
			sh "cd "+project_folder+" && git checkout  " + branch
			println(e1);
		}       
		try {
			sh "cd "+project_folder+" && git pull origin " + branch 
		}
		catch(Exception e1) {
			println(e1);
		}
        
        sh "cp -r "+project_folder+"/config.py ./beacon/server/config/."
	}
}
 
def BuildAndCopyMibsHere(branch, credentials,project_folder,content) {
	sh "rm -r -f "+project_folder
    withCredentials([string(credentialsId: credentials, variable: 'gitea_apapakon_token')]) {
    	// some block
		sh "git clone -c http.sslVerify=false -b " + "develop" + " https://" + gitea_token + ":x-oauth-basic@172.16.10.100/gitea/platform/"+project_folder+" "+project_folder
        sh "cd "+project_folder+" && git fetch --all"

		try {
			sh "cd "+project_folder+" && git checkout -b " + branch
		}
		catch(Exception e1) {
			sh "cd "+project_folder+" && git checkout  " + branch
			println(e1);
		}       
		try {
			sh "cd "+project_folder+" && git pull origin " + branch 
		}
		catch(Exception e1) {
			println(e1);
		}
	    
        sh ''' git config --global user.email "davide.piscia@cnag.eu"
              git config --global user.name "davide.piscia@cnag.eu" '''
        sh "cp "+content+" "+project_folder+"/."
        sh "cd "+project_folder+" && if [ \$(git status --porcelain | wc -l) -gt 0 ]; then git add * && git commit -m 'Latest build' -i * && git push origin " + branch + "; else echo 'No chanegs to commit'; fi"
            
    }
}


pipeline {
    agent {
        label 'any'
    }
    stages {
    	stage("none") {
	    	steps{
	    		sh 'ls'
	    	}
    	}

		stage('install requirements') {
            steps {    
                withPythonEnv('python3'){
					sh 'pip install pip==23.2.1'
					sh 'pip install -r requirements.txt'
                }
            }
        }

		stage('run test') {
			steps {
				withPythonEnv('python3'){
					withCredentials([string(credentialsId: 'gitea_config', variable: 'gitea_token')]) {
					//sh 'docker run --net=host --name postgres_test_flask -e POSTGRES_PASSWORD=mysecretpassword -d postgres'
					//sh "rm -rf beacon-v2-config"
					getConfigFromGitea(env.BRANCH_NAME,"gitea_apapakon_token","beacon-v2-config")
					sh 'pytest beacon/tests/test_*'
					//sh 'pytest --cov-report xml:phenostore_server/tests/coverage.xml --cov=. phenostore_server/tests/test_*'
					}

				}
			}
        }

		//stage('Sonarqube') {
			//environment {
			//	scannerHome = tool 'SQScanner'
			//	SONAR_SCANNER_OPTS = '-Djavax.net.ssl.trustStore=/home/ujenkins/cacerts -Djavax.net.ssl.trustStorePassword=changeit -Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=1044'
			//}
			//steps {
			//	withSonarQubeEnv('SQServer') {
			//		withCredentials([string(credentialsId: 'sonar-beaconv2-server', variable: 'sonar_beaconv2_server')]) {
			//			sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=beaconv2-server -Dsonar.login=${sonar_beaconv2_server}"
			//		}
			//	}
			//}
			//timeout(time: 10, unit: 'MINUTES') {
			//    waitForQualityGate abortPipeline: true
			//}
		//}
    }

    post {
        always {
        	archiveArtifacts artifacts: '*.*', fingerprint: true
        	withPythonEnv('python3') {
                sh 'tar -zcvf beacon_v2_server.tgz --exclude=__pycache__ beacon'
                BuildAndCopyMibsHere(env.BRANCH_NAME, 'gitea_apapakon_token','beacon_v2_artifact','beacon_v2_server.tgz')
            }
            slackSend color: "good", message: "Job: ${env.JOB_NAME} with buildnumber ${env.BUILD_NUMBER} was successful"
        }
    }
}
