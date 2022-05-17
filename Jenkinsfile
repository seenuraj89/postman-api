CODE_CHANGES = getGitChanges()
pipeline {
  agent any
  stages {
  stage('build') {
      steps {
        when {
          expression {
            BRANCH_NAME == 'master' && CODE_CHANGES == true
        script {
          echo 'building the application'
        }
      }
    }
  stage('test') {
      steps {
        when {
          expression {
            BRANCH_NAME == 'master'
        script {
          echo 'Stage 2'
        }
      }
    }
  }
}
