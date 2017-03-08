(function () {

    'use strict';

    /**
     * Project controller which manages creating a new project
     */
    angular
        .module('taskingManager')
        .controller('projectController', ['$location', 'mapService', 'projectService', projectController]);

    function projectController($location, mapService, projectService) {
        var vm = this;
        vm.project = null;
        vm.map = null;

        activate();

        function activate() {
            //TODO: Set up sidebar tabs

            mapService.createOSMMap('map');
            vm.map = mapService.getOSMMap();


            //TODO get projectId from URL, pattern /project{id}

            var id = $location.search().project;
            initialiseProject(id);

            //TODO: set project name on header

            //TODO: style the project on the map
            //TODO: put the project metadata (description instructions on disebar tabs

        }

        /**
         * Get a  project with using it's id
         */
        function initialiseProject(id){

            var resultsPromise = projectService.getProject(id);
            resultsPromise.then(function (data) {
                //project returned successfully
                vm.project = data;
                addProjectTasksToMap(vm.project.tasks);
            }, function(){
                // project not returned successfully
                // TODO - may want to handle error
            });

        };

        /**
         * Adds project tasks to map as features from geojson
         */
        function addProjectTasksToMap(tasks){
            //TODO: may want to refactor this into a service at some point so that it can be resused
            var source = new ol.source.Vector();
            var vector = new ol.layer.Vector({
                source: source
            });
            vm.map.addLayer(vector);

            // read tasks JSON into features
            var format = new ol.format.GeoJSON();
            var taskFeatures = format.readFeatures(tasks, {
                dataProjection: 'EPSG:4326',
                featureProjection: 'EPSG:3857'
            });
            source.addFeatures(taskFeatures);
            vm.map.getView().fit(source.getExtent());
        }
    }
})();
