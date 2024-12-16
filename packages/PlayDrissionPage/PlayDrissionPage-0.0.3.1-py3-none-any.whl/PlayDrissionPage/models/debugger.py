from PlayDrissionPage.models.base import CDPBaseModel
import pydantic


class evaluateOnCallFrameRQ(CDPBaseModel):

    call_frame_id: str
    expression: str
    object_group = None
    include_command_line_api = None
    silent = None
    return_by_value = True
    generate_preview = None
    throw_on_side_effect = None
    timeout = None


if __name__ == '__main__':
    z = evaluateOnCallFrameRQ(
        call_frame_id="call_frame_id",
        expression="expression",
    )
    print(z.model_dump())
    evaluateOnCallFrameRQ(
        call_frame_id="call_frame_id",
        expression="expression",
        object_group="object_group",
        include_command_line_api=True,
        silent=True,
        return_by_value=True,
        generate_preview=True,
        throw_on_side_effect=True,
        timeout="timeout",
    )
