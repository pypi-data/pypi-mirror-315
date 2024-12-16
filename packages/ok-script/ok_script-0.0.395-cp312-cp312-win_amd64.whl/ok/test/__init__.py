from ok.capture.Capture import ImageCaptureMethod

from ok.interaction.DoNothingInteraction import DoNothingInteraction

ok = None


def init_ok(config):
    global ok
    if ok is None:
        from ok.main.OK import OK
        config['debug'] = True
        ok = OK(config)
        ok.task_executor.debug_mode = True
        ok.device_manager.capture_method = ImageCaptureMethod(
            ok.device_manager.exit_event, [])
        ok.device_manager.interaction = DoNothingInteraction(
            ok.device_manager.capture_method)
        ok.app
