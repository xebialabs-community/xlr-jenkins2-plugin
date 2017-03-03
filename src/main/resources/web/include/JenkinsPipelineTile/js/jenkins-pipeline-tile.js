/*
 * THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
 * FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
 */
'use strict';

(function () {

    var ISPWTileController = function ($scope, ReleasesService, XlrTileHelper) {
        var vm = this;

        if ($scope.xlrDashboard) {
            // summary page
            vm.release = $scope.xlrDashboard.release;
            vm.tile = $scope.xlrTile.tile;
            vm.config = vm.tile.configurationProperties;
        } else {
            // details page
            vm.release = $scope.xlrTileDetailsCtrl.release;
            vm.tile = $scope.xlrTileDetailsCtrl.tile;
            vm.config = vm.tile.configurationProperties;
        }


        function load() {
            if (tileConfigurationIsPopulated()) {
                vm.allISPWTasks = getAllISPWTasks(vm.release, vm.config);
                vm.counts = XlrTileHelper.countTasksByStatus(vm.allISPWTasks);
                vm.totalCount = vm.allISPWTasks.length;
                vm.gridOptions = getGridOptions(vm.allISPWTasks);

                vm.chartOptions = XlrTileHelper.getChartOptions({
                    label: vm.config.action,
                    total: vm.totalCount
                });
            }
        }

        function getAllISPWTasks(release) {
            return _(ReleasesService.getLeafTasks(release))
                .filter({scriptDefinitionType: "ispwServices." + vm.config.action})
                .map(function (task) {
                    return {
                        taskName: task.title,
                        srId: task.inputProperties.srid,
                        application: task.inputProperties.appl,
                        relId: task.inputProperties.relid,
                        taskStatus: task.status,
                        taskStatusCategory: XlrTileHelper.getCategoryByTaskStatus(task.status)
                    };
                })
                .value();
        }

        function tileConfigurationIsPopulated() {
            return !_.isEmpty(vm.config.action);
        }

        function getGridOptions(allISPWTasks) {
            var columnDefs = [
                {
                    displayName: "Task",
                    field: "taskName",
                    cellTemplate: "static/@project.version@/include/ISPWTile/grid/ispw-name-cell-template.html",
                    filterHeaderTemplate: "<div data-ng-include=\"'partials/releases/grid/templates/name-filter-template.html'\"></div>",
                    enableColumnMenu: false,
                    width: '40%'
                },
                {
                    displayName: "SR ID",
                    field: "srId",
                    cellTemplate: "static/@project.version@/include/ISPWTile/grid/ispw-srid-cell-template.html",
                    filterHeaderTemplate: "<div data-ng-include=\"'partials/releases/grid/templates/name-filter-template.html'\"></div>",
                    enableColumnMenu: false,
                    width: '20%'
                },
                {
                    displayName: "Release ID",
                    field: "relId",
                    cellTemplate: "static/@project.version@/include/ISPWTile/grid/ispw-relid-cell-template.html",
                    filterHeaderTemplate: "<div data-ng-include=\"'partials/releases/grid/templates/name-filter-template.html'\"></div>",
                    enableColumnMenu: false,
                    width: '20%'
                },
                {
                    displayName: "Status",
                    field: "taskStatusCategory",
                    cellTemplate: "static/@project.version@/include/ISPWTile/grid/ispw-status-cell-template.html",
                    filterHeaderTemplate: "<div data-ng-include=\"'partials/releases/grid/templates/name-filter-template.html'\"></div>",
                    enableColumnMenu: false,
                    width: '20%'
                }
            ];
            return XlrTileHelper.getGridOptions(allISPWTasks, columnDefs);
        }

        load();

    };
    ISPWTileController.$inject = ['$scope', 'ReleasesService', 'XlrTileHelper'];

    angular.module('xlrelease.ISPWServices.tile', []);
    angular.module('xlrelease.ISPWServices.tile').controller('ispwServices.ISPWTileController', ISPWTileController);

})();