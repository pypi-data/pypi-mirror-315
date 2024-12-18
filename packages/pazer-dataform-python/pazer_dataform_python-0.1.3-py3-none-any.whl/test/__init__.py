
from pazer_dataform_python import ResponseForm

vms = ResponseForm()
vms.timer = True
vms.status = True
print(vms.toResponseJSON().body)
