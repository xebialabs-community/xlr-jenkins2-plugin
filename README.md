# xlr-jenkins2-plugin

This plugin offers an interface from XL Release to Jenkins 2.x. 

[![Build Status][xlr-jenkins2-plugin-travis-image]][xlr-jenkins2-plugin-travis-url]
[![Codacy Badge][xlr-jenkins2-plugin-codacy-image] ][xlr-jenkins2-plugin-codacy-url]
[![Code Climate][xlr-jenkins2-plugin-code-climate-image] ][xlr-jenkins2-plugin-code-climate-url]
[![License: MIT][xlr-jenkins2-plugin-license-image] ][xlr-jenkins2-plugin-license-url]
[![Github All Releases][xlr-jenkins2-plugin-downloads-image] ]()


[xlr-jenkins2-plugin-travis-image]: https://travis-ci.org/xebialabs-community/xlr-jenkins2-plugin.svg?branch=master
[xlr-jenkins2-plugin-travis-url]: https://travis-ci.org/xebialabs-community/xlr-jenkins2-plugin
[xlr-jenkins2-plugin-codacy-image]: https://api.codacy.com/project/badge/Grade/a6f64efd62f341acb50f67c511d3fb42
[xlr-jenkins2-plugin-codacy-url]: https://www.codacy.com/app/joris-dewinne/xlr-jenkins2-plugin
[xlr-jenkins2-plugin-code-climate-image]: https://codeclimate.com/github/xebialabs-community/xlr-jenkins2-plugin/badges/gpa.svg
[xlr-jenkins2-plugin-code-climate-url]: https://codeclimate.com/github/xebialabs-community/xlr-jenkins2-plugin
[xlr-jenkins2-plugin-license-image]: https://img.shields.io/badge/License-MIT-yellow.svg
[xlr-jenkins2-plugin-license-url]: https://opensource.org/licenses/MIT
[xlr-jenkins2-plugin-downloads-image]: https://img.shields.io/github/downloads/xebialabs-community/xlr-jenkins2-plugin/total.svg


## Usage

### Triggers

You can configure a job trigger by first going to your template and selecting `Triggers`. You can use 2 trigger types:

  * JobTrigger: Polls for a Jenkins Job to finish
  * FolderTrigger: Polls for any Jenkins job(s) to finish underneath a Jenkins folder
  
  ![Jenkins Trigger](images/jenkins_trigger.png)
  
  When selected, you can provide the Jenkins details.
  ![Jenkins Trigger Details](images/jenkins_trigger_details.png)
 
### Tiles
    * **Jenkins Job Summary Tile:**
    This tile can be used to pull a summary of all runs of a jenkins job
    
    **Configure Tile**
    ![Configure tile](images/jenkins_jobsummarytile_configure.png)
    
    **Preview Tile**
    ![Configure tile](images/jenkins_jobsummarytile.png)

    * **Jenkins Pipeline View Tile:

    This tile breaks down the build time for recent jobs, down to the level of build stages.  Users can quickly identify skipped stages, outlier build times, and build performance degradation.

    ** The [Pipeline Stage View Jenkins Plugin](https://github.com/jenkinsci/pipeline-stage-view-plugin) must be installed in Jenkins, before using this dashboard tile. **

### Tasks 
    * Jenkins.GetBuildParameters tasks allows to fetch the parameters from an executed job.
    ![Jenkins GetBuildParameters](images/jenkins_get_parameters.png) 

## Testing and Development
If you want to start this plugin, you could use the following command `./gradlew runDockerCompose`. 
This will give you 2 containers (Jenkins and XL Release), with the plugin preloaded.

* How to retrieve the admin password for jenkins? 

`docker exec -it docker_jenkins_1 cat /var/jenkins_home/secrets/initialAdminPassword` 

## Contributing

Please review the contributing guidelines for _xebialabs-community_ at [http://xebialabs-community.github.io/](http://xebialabs-community.github.io/)

## License

This community plugin is licensed under the [MIT license][xlr-jenkins2-plugin-license-url].

See license in [License.md](License.md)