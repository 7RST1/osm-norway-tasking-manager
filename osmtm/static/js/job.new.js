var map = null,
    vectorLayer = null,
    tiles = null;

function updateSubmitBtnStatus() {
    var disabled = $('#id_title').val() === '' ||
        $('#geometry').val() === '';
    $('#id_submit')[0].disabled = disabled;
}

$('#id_title').focus();


$('#id_title')
    .change(function() {
        updateSubmitBtnStatus();
    });

var map = L.map('map').setView([0, 0], 0);
// create the tile layer with correct attribution
var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
var osmAttrib='Map data © OpenStreetMap contributors';
var osm = new L.TileLayer(osmUrl, {attribution: osmAttrib, drawControl: true});
map.addLayer(osm);

var drawControl = new L.Control.Draw({
    position: 'topleft',
    rectangle: false,
    circle: false,
    marker: false,
    polyline: false,
    polygon: {
        title: 'Draw the area of interest'
    }
});
map.addControl(drawControl);

var vector = new L.LayerGroup();
map.on('draw:poly-created', function(e) {
    vector.addLayer(e.poly);
    $('#geometry').val(toGeoJSON(e.poly));
    updateSubmitBtnStatus();
});
map.on('drawing', function(e) {
    vector.clearLayers();
    $('#geometry').val('');
    updateSubmitBtnStatus();
});
map.addLayer(vector);


var toGeoJSON = function(polygon) {
    var json, type, latlng, latlngs = [], i;

    type = 'Polygon';
    latlngs = LatLngsToCoords(polygon._latlngs, 1);
    return JSON.stringify({"type": type, "coordinates": [latlngs]});
};

var LatLngToCoords = function (LatLng, reverse) { // (LatLng, Boolean) -> Array
    var lat = parseFloat(reverse ? LatLng.lng : LatLng.lat),
        lng = parseFloat(reverse ? LatLng.lat : LatLng.lng);

    return [lng,lat];
};

var LatLngsToCoords = function (LatLngs, levelsDeep, reverse) { // (LatLngs, Number, Boolean) -> Array
    var coord,
        coords = [],
        i, len;

    for (i = 0, len = LatLngs.length; i < len; i++) {
        coord = levelsDeep ?
                LatLngToCoords(LatLngs[i], levelsDeep - 1, reverse) :
                LatLngToCoords(LatLngs[i], reverse);
        coords.push(coord);
    }

    return coords;
};
