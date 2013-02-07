<%inherit file="/base.mako"/>
<%def name="id()">home</%def>
<%def name="title()">Home Page</%def>
<div class="container">
    <div class="row">
        % for map in maps:
            ${map_item(map)}
        % endfor
    </div>
</div>


<%def name="map_item(map)">
    <div id="maps" data-bind="foreach: maps">
        <div class="map well">
            <ul class="nav map-stats">
                <li>
                    <i class="icon-user"></i>
                    <span></span>
                </li>
                <li class="row">
                    <table>
                        <tr>
                            <td>
                                <div class="progress"
                                     style="border: 1px solid #ccc">
                                    <div class="bar" style="width: 90%"></div>
                                </div>
                            </td>
                            <td></td>
                        </tr>
                    </table>
                </li>
            </ul>
            <h4>
                <a href="${request.route_url('map', map=map.id)}">${map.title}</a>
            </h4>
            <div class="clear"></div>
            <div class="created-by">
                Created by <span>Pierre</span>
            </div>
            <div class="world_map">
                <div class="marker" style="top: 15px;left: 43px"></div>
            </div>
            <div class="clear"></div>
            <div class="updated-at">
                Updated <span>10 min</span> ago
            </div>
        </div>
    </div>
</%def>
