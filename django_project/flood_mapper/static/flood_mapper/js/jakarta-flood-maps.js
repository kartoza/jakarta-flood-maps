/**
 * Created by ismailsunni on 1/13/15.
 */
/*global $, jQuery, L, window, console*/
var map;

jQuery.download = function (url, data, method) {
    /* Taken from http://www.filamentgroup.com/lab/jquery-plugin-for-requesting-ajax-like-file-downloads.html*/
    'use strict';
    //url and data options required
    if (url && data) {
        //data can be string of parameters or array/object
        data = typeof data === 'string' ? data : jQuery.param(data);
        //split params into form inputs
        var inputs = '';
        jQuery.each(data.split('&'), function () {
            var pair = this.split('=');
            inputs += '<input type="hidden" name="' + pair[0] + '" value="' + pair[1] + '" />';
        });
        //send request
        jQuery('<form action="' + url + '" method="' + (method || 'post') + '">' + inputs + '</form>')
            .appendTo('body').submit().remove();
    }
};

function toggle_side_panel() {
    'use strict';
    var map_div = $('#map'),
        side_panel = $('#side_panel'),
        show_hide_div = $('#show_hide');
    /* hide */
    if (side_panel.is(":visible")) {
        show_hide_div.removeClass('glyphicon-chevron-right');
        show_hide_div.addClass('glyphicon-chevron-left');
        side_panel.removeClass('col-lg-4');
        side_panel.hide();
        map_div.removeClass('col-lg-8');
        map_div.addClass('col-lg-12');
        map.invalidateSize();
    } else { /* show */
        show_hide_div.addClass('glyphicon-chevron-right');
        show_hide_div.removeClass('glyphicon-chevron-left');
        side_panel.addClass('col-lg-4');
        side_panel.show();
        map_div.removeClass('col-lg-12');
        map_div.addClass('col-lg-8');
        map.invalidateSize();
    }
}

function show_map() {
    'use strict';
    $('#navigationbar').css('height', window.innerHeight * 0.1);
    $('#map').css('height', window.innerHeight * 0.9);
    map = L.map('map').setView([-6.2000, 106.8167], 11);
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

}

function update_rws() {
    'use strict';
    var village_select = $('#id_village'),
        village_id = village_select.val(),
        rw_select = $('#id_rw'),
        rt_select = $('#id_rt');
    rw_select.find('option').remove().end();
    rw_select.append($("<option></option>")
        .attr("value", '')
        .text('---------'));
    rt_select.find('option').remove().end();
    rt_select.append($("<option></option>")
        .attr("value", '')
        .text('---------'));
    if (village_id === '') {
        return;
    }
    village_select.attr("disabled", "disabled");
    $.get('/api/locations/' + village_id + '/?format=json', function (data) {
        /*jslint unparam: true*/
        $.each(data, function (dummy, rw) {
            $('#id_rw').append($("<option></option>")
                .attr("value", rw.id)
                .text(rw.name));
        });
        /*jslint unparam: false*/
        village_select.removeAttr("disabled");
    });
}

function update_rts() {
    'use strict';
    var village_id = $('#id_village').val(),
        rw_select = $('#id_rw'),
        rw_id = rw_select.val(),
        rt_select = $('#id_rt');
    rt_select.find('option').remove().end();
    rt_select.append($("<option></option>")
        .attr("value", '')
        .text('---------'));
    if ((village_id === '') || (rw_id === '')) {
        return;
    }
    rw_select.attr("disabled", "disabled");
    $.get('/api/locations/' + village_id + '/' + rw_id + '/?format=json',
        function (data) {
            /*jslint unparam: true*/
            $.each(data, function (dummy, rt) {
                $('#id_rt').append($("<option></option>")
                    .attr("value", rt.id)
                    .text(rt.name));
            });
            /*jslint unparam: false*/
            rw_select.removeAttr("disabled");
        });
}


function update_rts_rws() {
    'use strict';
    $('#nav_add_flood_status_report').addClass("active");
    // Setup location selecton
    $('#id_village').on('change', update_rws);
    $('#id_rw').on('change', update_rts);
    // Setup date time picker
    var date_time = $('#id_date_time');
    date_time.datetimepicker({
        format: 'YYYY-MM-DD HH:mm'
    });
}

function updateFloodAreaReport() {
    'use strict';
    var rt = $('#rt'),
        rt_id;
    rt.prop('disabled', 'disabled');
    rt_id = rt.val();
    $.get('/api/reports/rt/' + rt_id + '/?format=json', function (data) {
        if (data.length === 0) {
            console.log('No reported flood info');
        } else {
            $('#current_flood_depth').text(data[0].depth);
            $('#current_flood_depth_div').show();
        }
        rt.prop('disabled', false);
    });
}

function updateFloodAreaOptions(rw_id, rw_name) {
    'use strict';
    $('#rw').text(rw_name);
    $('#village').text('');
    var rt_select = $('#rt');
    rt_select.find('option').remove().end();
    rt_select.append($("<option></option>")
        .attr("value", '')
        .text('---------'));
    $.get('/api/village/' + rw_id + '/?format=json', function (data) {
        $('#village').text(data.name);
        var village_id = data.id;
        $.get('/api/locations/' + village_id + '/' + rw_id + '/?format=json', function (data) {
            /*jslint unparam: true*/
            $.each(data, function (dummy, rt) {
                rt_select.append($("<option></option>")
                    .attr("value", rt.id)
                    .text(rt.name));
            });
            /*jslint unparam: false*/
        });
    });
}

/*jslint unparam: true*/
function style(feature) {
    'use strict';
    return {
        weight: 2,
        opacity: 1,
        color: 'blue',
        dashArray: '3',
        fillOpacity: 0.5,
        fillColor: 'blue'
    };
}
/*jslint unparam: false*/

function highlightFeature(e) {
    'use strict';
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
    'use strict';
    var layer = e.target;
    layer.setStyle(style(e));
}

function zoomToFeature(e) {
    'use strict';
    var rw_id, rw_name, layer;
    layer = e.target;
    map.fitBounds(layer.getBounds());
    $('#select_rw').hide();
    $('#staff_details').hide();
    $('#current_flood_depth_div').hide();
    $('#details').show();
    if (window.location.pathname === '/') {
        toggle_side_panel();
    }

    rw_id = layer.options.properties.rw_id;
    rw_name = layer._options.properties.name;
    updateFloodAreaOptions(rw_id, rw_name);
}

/*jslint unparam: true*/
function onEachFeature(feature, layer) {
    'use strict';
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: zoomToFeature
    });
}
/*jslint unparam: false*/

function setOffset() {
    'use strict';
    var navbar, navbar_height, map, content, map_offset, content_offset;
    navbar = $('.navbar');
    navbar_height = navbar.height();
    map = $('#map');
    content = $('#content');

    if (map.length) {
        map_offset = map.offset();
        map.offset({top: navbar_height, left: map_offset.left});
    }
    if (content.length) {
        content_offset = content.offset();
        content.offset({top: navbar_height, left: content_offset.left});
    }

}

function add_rw_to_map(time_slice, selected_rw) {
    $.get('/api/locations/flooded/rw/' + time_slice + '/?format=json', function (data) {
        /*jslint unparam: true*/
        var layer, rw_layer;
        $.each(data, function (dummy, rw_id) {
            $.get('/api/rw/' + rw_id + '/?format=json', function (rw) {
                rw_layer = JSON.parse(rw.geometry);
                layer = L.geoJson(rw_layer, {
                    style: style,
                    onEachFeature: onEachFeature,
                    properties: {
                        rw_id: rw.id,
                        name: rw.name,
                        population: rw.population
                    }
                }).addTo(map);
                if (rw_id === selected_rw) {
                    map.fitBounds(layer.getBounds());
                }
            });
        });
        /*jslint unparam: false*/
    });
}
