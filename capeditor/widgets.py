from django import forms
from django.template.loader import render_to_string
import json
from django.utils.functional import cached_property


class BasemapPolygonWidget(forms.HiddenInput):
    template_name = "capeditor/widgets/basemap_polygon.html" 

    @cached_property
    def media(self):
        return forms.Media(
            css={
                "all": (
                    "https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.css",
                    "https://unpkg.com/leaflet@1.7.1/dist/leaflet.css",
                    
                )
            },
            js=(
                "https://unpkg.com/leaflet@1.7.1/dist/leaflet.js",
                "https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.js",

            ),
        )

    def get_context(self, name, value, attrs=None):
        context = super().get_context(name, value, attrs)
        context['map_id'] = f'map-{name}'
        
        # if value:

        #     g1 = shapely.wkt.loads(value.ewkt.split(';')[1])

        #     g2 = geojson.Feature(geometry=g1, properties={})
        #     print("Vaaaaaalllluuuuu",json.dumps(g2.geometry.coordinates[0]))

        #     context['polygons'] = json.dumps(g2.geometry.coordinates[0]) if value else json.dumps([])
        #     return context

        return context

