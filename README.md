# odoo-16-popup-widget 
# Web module has to be installed.
This widget is an odoo popup widget that displays a popup box for a model in a tree view. It uses odoo owl and rpc.

usage: 
model:
name = fields.Char()


form view:
<field name="name" widget="popup_widget" relatedModel="modulename.modelname" relatedAction="method_in_python"/>
e.g. 
<field name="name" widget="z_popup.student" relatedAction="get_name"/>

name: name in model
widget = widget name
relatedAction = method in another model

# method in another model be like:
another model:

class Someone(models.Model):
  _name = 'modulename.modelname'
  
  name = fields.Char()
  email = fields.Char()

@api.model
def get_name(self)
  record = self.browse(record_id)
    return {
      'name': record.name,
      'email': record.email,
   }

## Note! the method must return a dictonary or might cause error.
## Do not forget to give access to 'another model' in the csv.
$ The get_name method will send the dictionary values to the rpc to fetch data at fronetnd.
