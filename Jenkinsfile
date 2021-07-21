def getSchemaFromGitea(branch, credentials,project_folder) {
	sh "rm -r -f "+project_folder
    withCredentials([string(credentialsId: credentials, variable: 'gitea_token')]) {
    	// some block 
        sh "git clone -c http.sslVerify=false -b " + "develop" + " https://" + gitea_token + ":x-oauth-basic@172.16.10.100/gitea/platform/"+project_folder
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
		sh "git clone -c http.sslVerify=false -b " + "develop" + " https://" + gitea_token + ":x-oauth-basic@172.16.10.100/gitea/platform/"+project_folder
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
        
        //sh "cp -r "+project_folder+"/config_test.py ./phenostore_server/config/."
        sh "cp -r "+project_folder+"/config.py ./beacon/server/config/."
	}
}
 
def BuildAndCopyMibsHere(branch, credentials,project_folder,content) {
	sh "rm -r -f "+project_folder
    withCredentials([string(credentialsId: credentials, variable: 'gitea_token')]) {
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
        
        sh "cp "+content+" "+project_folder+"/."
        sh "cd "+project_folder+" && if [ \$(git status --porcelain | wc -l) -gt 0 ]; then git add * && git commit -m 'Latest build' -i * && git push origin " + branch + "; else echo 'No chanegs to commit'; fi"
            
    }
}


pipeline {
    agent {
        label 'rdjenkins'
    }
    stages {
    	stage("none") {
	    	steps{
	    		sh 'ls'
	    	}
    	}
    }

    post {
        always {
        	archiveArtifacts artifacts: '*.*', fingerprint: true
        	withPythonEnv('python3') {
                sh 'tar -zcvf beacon_v2_server.tgz --exclude=__pycache__ beacon'
                BuildAndCopyMibsHere(env.BRANCH_NAME, 'gitea_config','beacon_v2_artifact','beacon_v2_server.tgz')
            }
            slackSend color: "good", message: "Job: ${env.JOB_NAME} with buildnumber ${env.BUILD_NUMBER} was successful"
        }
    }
}