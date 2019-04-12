from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2
import jinja2
import os
from models import GpuDevice
import logging

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class DisplayFeaturesGpu(webapp2.RequestHandler):
    def get(self, gpu_device_name):
        self.response.headers['Content-Type'] = 'text/html'
        url = ''
        gpu_all_data = GpuDevice.query(GpuDevice.name == gpu_device_name).get()

        template_values = {
            'url': url,
            'gpu_all_data': gpu_all_data,

        }

        template = JINJA_ENVIRONMENT.get_template('feature.html')
        self.response.write(template.render(template_values))

class GpuFeaturesQuerying (webapp2.RequestHandler):
    def post(self, *args, **kwargs):

            if len(self.request.POST.keys()) == 0:
                self.redirect('/')
            else:
                key = self.request.POST.keys()[0]
                logging.info(key)
                logging.info(self.request.POST[key])
                value = eval(self.request.POST[key])
                logging.info(value)
                gpu_device = None
            user = users.get_current_user()
            if user:
                url = users.create_logout_url(self.request.uri)
                url_string = 'logout'
                gpu_device = GpuDevice.query(ndb.BooleanProperty(key)==value).fetch()
            else:
                url = users.create_login_url(self.request.uri)
                url_string = 'login'

            template_values = {
                'url': url,
                'url_string': url_string,
                'user': user,
                'gpu_device': gpu_device,
                'filter_key' : key,
                'filter_value' : value
            }

            template = JINJA_ENVIRONMENT.get_template('main.html')
            self.response.write(template.render(template_values))


class AddGpuDetails(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        gpu_device_key = ndb.Key('GpuDevice', user.user_id())
        gpu_device = gpu_device_key.get()
        template_values = {
            'gpu_device': gpu_device
        }
        template = JINJA_ENVIRONMENT.get_template('AddDetaisGpu.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        if self.request.get('button') == 'Add':
            name = self.request.get('users_name')
            driver_device = float(self.request.get('driver_device'))
            api = float(self.request.get('api'))
            vendor_device = self.request.get('vendor_device')
            version_device = float(self.request.get('version_device'))
            type = self.request.get('type')
            platform_device = self.request.get('platform_device')
            geometry_shader = bool(self.request.get('GeometryShader'))
            tesselation_shader = bool(self.request.get('TesselationShaderr'))
            shader_int16 = bool(self.request.get('ShaderInt16'))
            sparse_binding = bool(self.request.get('SparseBinding'))
            texture_compressionetc2 = bool(self.request.get('TextureCompressionETC2'))
            vertex_pipeline_stores_and_atomics = bool(self.request.get('vertexPipelineStoresAndAtomics'))
            if GpuDevice.query(GpuDevice.name==name).get():
                 self.response.headers['Content-Type'] = 'text/html'
                 user = users.get_current_user()
                 template_values = {
                 "error" : "The Device Name already exists. Please enter another device name."
                 }
                 template = JINJA_ENVIRONMENT.get_template('AddDetaisGpu.html')
                 self.response.write(template.render(template_values))
            else :
                update_gpu_details = GpuDevice(name=name, driver_device=driver_device, version_device=version_device, api=api, vendor_device=vendor_device,
                                    type=type, platform_device=platform_device, geometry_shader=geometry_shader,
                                  tesselation_shader=tesselation_shader, shader_int16=shader_int16,
                                  sparse_binding=sparse_binding, texture_compressionetc2=texture_compressionetc2,
                                  vertex_pipeline_stores_and_atomics=vertex_pipeline_stores_and_atomics)
                update_gpu_details.put()
                self.redirect('/')
        elif self.request.get('button') == 'Cancel':
            self.redirect('/')
