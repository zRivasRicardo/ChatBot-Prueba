from behave import given, when, then
from helper.Comparative import Snapshots


@then(u'valido que la vista "{ruta}" no haya sufrido cambios')
def step_impl(context, ruta):
    validador = Snapshots.Snapshot.validateSnapshots(context, ruta)
    assert validador, "Los screenshots no coinciden"
