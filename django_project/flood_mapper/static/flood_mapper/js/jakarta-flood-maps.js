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
    var village_id = $('#id_village').val();
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
    $.get('/api/locations/' + village_id + '/?format=json', function(data){
        $.each(data, function(dummy, rw){
            $('#id_rw').append($("<option></option>")
                .attr("value", rw['id'])
                .text(rw['name']));
        });
    });
}
function update_rts(){
    var village_id = $('#id_village').val();
    var rw_id = $('#id_rw').val();
    var rt_select = $('#id_rt');
    rt_select.find('option').remove().end();
    rt_select.append($("<option></option>")
        .attr("value", '')
        .text('---------'));
    if ((village_id == '') || (rw_id == '')){
        console.log('returning');
        return;
    }
    $.get('/api/locations/' + village_id + '/' + rw_id + '/?format=json',
        function(data){
            $.each(data, function(dummy, rt){
                $('#id_rt').append($("<option></option>")
                    .attr("value", rt['id'])
                    .text(rt['name']));
            });
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