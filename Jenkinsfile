CODE_CHANGES = getGitChanges()
pipeline {
  agent any
  stages {
    stage("build") {
      when {
        expression {
          BRANCH_NAME == 'master' && CODE_CHANGES == true
        }
      }
      steps {
        echo 'building the application'
      }
    }
  }
}
