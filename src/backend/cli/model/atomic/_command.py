from cli.model.atomic._fields import CLICommandNameField, CLIStageField, CLIVersionField
from cli.model.atomic._help import CLICommandHelp
from cli.model.atomic._resource import CLISpecsResource
from schematics.models import Model
from schematics.types import ModelType, ListType


class CLIAtomicCommandRegisterInfo(Model):
    stage = CLIStageField(required=True)
    # TODO: add support for deprecate_info


class CLIAtomicCommand(Model):
    names = ListType(field=CLICommandNameField(), min_size=1, required=True)  # full name of a command
    help = ModelType(CLICommandHelp, required=True)
    register_info = ModelType(CLIAtomicCommandRegisterInfo, required=False)  # register info in command table. If it's not registered in command table, this field is None

    version = CLIVersionField(required=True)
    resources = ListType(ModelType(CLISpecsResource), required=True, min_size=1)

    class Options:
        serialize_when_none = False
