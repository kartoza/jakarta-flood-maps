/**
 * Created by ismailsunni on 1/13/15.
 */
var map;

function show_side_panel(){
    var map_div = $('#map');
    var side_panel = $('#side_panel');
    var show_hide_div = $('#show_hide');
    var show_hide_div_sub = $(show_hide_div.children()[0]);
    var show_hide_glyph = $('#show_hide_glyph');
    show_hide_div.addClass('col-xs-offset-7');
    show_hide_div.removeClass('col-xs-offset-11');
    show_hide_div_sub.addClass('col-xs-offset-11');
    show_hide_div_sub.removeClass('col-xs-offset-7');
    show_hide_div_sub.attr("onclick", "hide_side_panel()");
    show_hide_glyph.removeClass('glyphicon-chevron-left');
    show_hide_glyph.addClass('glyphicon-chevron-right');
    map_div.addClass('col-xs-8');
    side_panel.addClass('col-xs-4');
    side_panel.show();
    map_div.removeClass('col-xs-12');
    map.invalidateSize();
}

function hide_side_panel(){
    var map_div = $('#map');
    var side_panel = $('#side_panel');
    var show_hide_div = $('#show_hide');
    var show_hide_div_sub = $(show_hide_div.children()[0]);
    var show_hide_glyph = $('#show_hide_glyph');
    show_hide_div.addClass('col-xs-offset-11');
    show_hide_div.removeClass('col-xs-offset-7');
    show_hide_div_sub.addClass('col-xs-offset-7');
    show_hide_div_sub.removeClass('col-xs-offset-11');
    show_hide_div_sub.attr("onclick", "show_side_panel()");
    show_hide_glyph.removeClass('glyphicon-chevron-right');
    show_hide_glyph.addClass('glyphicon-chevron-left');
    map_div.addClass('col-xs-12');
    side_panel.removeClass('col-xs-4');
    side_panel.hide();
    map_div.removeClass('col-xs-8');
    map.invalidateSize();
}

function show_map() {
    $('#navigationbar').css('height', window.innerHeight * 0.1);
    $('#map').css('height', window.innerHeight * 0.9);
    map = L.map('map').setView([-6.2000, 106.8167], 11);
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

}

function update_rws(){
  var village_select = $('#id_village');
  var village_id = village_select.val();
  var rw_select = $('#id_rw');
  var rt_select = $('#id_rt');
  rw_select.find('option').remove().end();
  rw_select.append($("<option></option>")
    .attr("value", '')
    .text('---------'));
  rt_select.find('option').remove().end();
  rt_select.append($("<option></option>")
    .attr("value", '')
    .text('---------'));
  if (village_id == ''){
    return;
  }
  village_select.attr("disabled", "disabled");
  $.get('/api/locations/' + village_id + '/?format=json', function(data){
    $.each(data, function(dummy, rw){
      $('#id_rw').append($("<option></option>")
       .attr("value", rw['id'])
       .text(rw['name']));
    });
    village_select.removeAttr("disabled");
  });
}

function update_rts(){
  var village_id = $('#id_village').val();
  var rw_select = $('#id_rw');
  var rw_id = rw_select.val();
  var rt_select = $('#id_rt');
  rt_select.find('option').remove().end();
  rt_select.append($("<option></option>")
    .attr("value", '')
    .text('---------'));
  if ((village_id == '') || (rw_id == '')){
    console.log('returning');
    return;
  }
  rw_select.attr("disabled", "disabled");
  $.get('/api/locations/' + village_id + '/' + rw_id + '/?format=json',
        function(data){
    $.each(data, function(dummy, rt){
      $('#id_rt').append($("<option></option>")
       .attr("value", rt['id'])
       .text(rt['name']));
    });
    rw_select.removeAttr("disabled");
  });
}


function update_rts_rws(){
    $('#nav_add_flood_status_report').addClass("active");
    // Setup location selecton
    $('#id_village').on('change', update_rws);
    $('#id_rw').on('change', update_rts);
    // Setup date time picker
    var date_time = $('#id_date_time');
    date_time.datetimepicker(
        {
            format: 'YYYY-MM-DD HH:mm'
        });
}

function updateFloodAreaReport(){
  var rt = $('#rt');
  rt.prop('disabled', 'disabled');
  var rt_id = rt.val();
  $.get('/api/reports/rt/' + rt_id + '/?format=json', function(data){
    console.log(data);
    if (data.length == 0){
      console.log('No reported flood info');
    } else {
      $('#current_flood_depth').text(data[0]["depth"]);
      $('#current_flood_depth_div').show();
    }
    rt.prop('disabled', false);
  })
}

function updateFloodAreaOptions(rw_id, rw_name){
  $('#rw').text(rw_name);
  $('#village').text('');
  var rt_select = $('#rt');
  rt_select.find('option').remove().end();
  rt_select.append($("<option></option>")
    .attr("value", '')
    .text('---------'));
  $.get('/api/village/' + rw_id + '/?format=json', function(data){
    $('#village').text(data['name']);
    var village_id = data['id'];
    $.get('/api/locations/' + village_id + '/' +rw_id + '/?format=json', function(data) {
       $.each(data, function(dummy, rt) {
         rt_select.append($("<option></option>")
           .attr("value", rt['id'])
           .text(rt['name']));
       });
    });
  });
}

function style(feature) {
    return {
        weight: 2,
        opacity: 1,
        color: 'blue',
        dashArray: '3',
        fillOpacity: 0.5,
        fillColor: 'blue'
    };
}

function highlightFeature(e) {
    var layer = e.target;
    layer.setStyle({
        weight: 5,
        color: 'white',
        dashArray: '',
        fillOpacity: 0.3,
        fillColor: 'blue'
    });
    if (!L.Browser.ie && !L.Browser.opera) {
        layer.bringToFront();
    }
}

function resetHighlight(e) {
    var layer = e.target;
    layer.setStyle(style(e));
}

function zoomToFeature(e) {
    var layer = e.target;
    map.fitBounds(layer.getBounds());
    $('#select_rw').hide();
    $('#staff_details').hide();
    $('#current_flood_depth_div').hide();
    $('#details').show();
    if (window.location.pathname == '/'){
        show_side_panel();
    }

    console.log(layer);
    var rw_id = layer["_options"]["properties"]["rw_id"];
    var rw_name = layer["_options"]["properties"]["name"];
    updateFloodAreaOptions(rw_id, rw_name);
}

function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: zoomToFeature
    });
}

function setOffset(){
    var navbar = $('.navbar');
    var navbar_height = navbar.height();
    var map = $('#map');
    var content = $('#content');

    if (map.length){
        var map_offset = map.offset();
        map.offset({ top: navbar_height, left: map_offset.left})
    }
    if (content.length){
        var content_offset = content.offset();
        content.offset({ top: navbar_height, left: content_offset.left})
    }

}

function add_rw_to_map(time_slice){
  var selected_rw;
  if (time_slice != 'current') {
    var query = window.location.search.substring(1);
    if (query.length > 0) {
      var rw = query.split('&')[0].split('=');
      if (rw[0] == 'rw') {
        selected_rw = rw[1];
      }
    }
  }
  $.get('/api/locations/flooded/rw/' + time_slice + '/?format=json', function(data){
    $.each(data, function(dummy, rw_id){
      $.get('/api/rw/' + rw_id + '/?format=json', function(rw){
          var rw_layer = JSON.parse(rw['geometry']);
          var layer = L.geoJson(rw_layer, {
            style: style,
            onEachFeature: onEachFeature,
            properties: {
              rw_id: rw['id'],
              name: rw['name'],
              population: rw['population']
            }
          }).addTo(map);
          if (rw_id == selected_rw){
            map.fitBounds(layer.getBounds());
          }
      });
    });
  });
}
