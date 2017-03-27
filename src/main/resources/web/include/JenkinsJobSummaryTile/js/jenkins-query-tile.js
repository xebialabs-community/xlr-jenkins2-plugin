/*
 * THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
 * FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
 */

'use strict';

(function () {

    var JenkinsSummaryTileViewController = function ($scope, JenkinsSummaryService, XlrTileHelper) {
        var vm = this;

        vm.tileConfigurationIsPopulated = tileConfigurationIsPopulated;

        var tile;

        var predefinedColors = [];
        predefinedColors['SUCCESS'] = 'green';
        predefinedColors['FAILURE'] = 'red';


        if ($scope.xlrTile) {
            // summary mode
            tile = $scope.xlrTile.tile;
        }

        function getColor(value) {
            if (predefinedColors[value]) return predefinedColors[value];
        }

        function tileConfigurationIsPopulated() {
            var config = tile.configurationProperties;
            return !_.isEmpty(config.jenkinsServer);
        }

        function getTitle(){
            if(vm.issuesSummaryData.total > 1){
                return "jobs";
            }
            else{
                return "job";
            }
        }

        vm.chartOptions = {
            topTitleText: function (data) {
                return data.total;
            },
            bottomTitleText: getTitle,
            series: function (data) {
                var series = {
                    name: 'State',
                    data: []
                };
                series.data = _.map(data.data, function (value) {
                    return {y: value.counter, name: value.state, color: value.color};
                });
                return [ series ];
            },
            showLegend: true,
            donutThickness: '60%'
        };

        function load(config) {
            if (tileConfigurationIsPopulated()) {
                vm.loading = true;
                JenkinsSummaryService.executeQuery(tile.id, config).then(
                    function (response) {
                        $scope.xlrTile.title = $scope.xlrTile.title + " : " + tile.configurationProperties.jobName
                        var serviceNowIssueArray = [];
                        var issues = response.data.data;
                        if(issues[0] === "Invalid table name"){
                            vm.invalidTableName = true;
                        }
                        else{
                            vm.invalidTableName = false;
                            vm.states = [];
                            vm.statesCounter = 0;
                            vm.issuesSummaryData = {
                                data: null,
                                total: 0
                            };
                            vm.issuesSummaryData.data = _.reduce(issues, function (result, value) {
                                var state = value.result;
                                vm.issuesSummaryData.total += 1;
                                if (result[state]) {
                                    result[state].counter += 1;
                                } else {
                                    result[state] = {
                                        counter: 1,
                                        color: getColor(state),
                                        state: state
                                    };
                                }
                                return result;

                            }, {});
                            _.forEach(vm.issuesSummaryData.data, function (value, key) {
                                if (vm.statesCounter < 5) vm.states.push(value);
                                vm.statesCounter++;
                            });
                        }
                    }
                    ).finally(function () {
                        vm.loading = false;

                    });
                }
            }


            function refresh() {
                load({params: {refresh: true}});
            }

            load();

            vm.refresh = refresh;
        };

        JenkinsSummaryTileViewController.$inject = ['$scope', 'xlrelease.jenkins.JenkinsSummaryService', 'XlrTileHelper'];

        var JenkinsSummaryService = function (Backend) {

            function executeQuery(tileId, config) {
                return Backend.get("tiles/" + tileId + "/data", config);
            }

            return {
                executeQuery: executeQuery
            };
        };

        JenkinsSummaryService.$inject = ['Backend'];

        angular.module('xlrelease.jenkinssummary.tile', []);
        angular.module('xlrelease.jenkinssummary.tile').service('xlrelease.jenkins.JenkinsSummaryService', JenkinsSummaryService);
        angular.module('xlrelease.jenkinssummary.tile').controller('jenkins.JenkinsSummaryTileViewController', JenkinsSummaryTileViewController);

    })();

