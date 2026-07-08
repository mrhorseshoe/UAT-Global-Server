from bot.base.manifest import APP_MANIFEST_LIST
from bot.engine.scheduler import scheduler
from bot.conn.u2_ctrl import U2AndroidController
from module.umamusume.asset.point import *


def start():
    scheduler.start()


def stop():
    scheduler.stop()


def toggle_stop_after_run():
    scheduler.stop_after_run = not getattr(scheduler, 'stop_after_run', False)
    return scheduler.stop_after_run


def get_status():
    if scheduler.active:
        status = "finishing" if scheduler.stop_after_run else "running"
    else:
        status = "stopped"
    return {"status": status, "stop_after_run": bool(scheduler.stop_after_run)}


def add_task(app_name, task_execute_mode, task_type, task_desc, cron_job_config, attachment_data):
    app_config = APP_MANIFEST_LIST[app_name]
    task = app_config.build_task(task_execute_mode, task_type, task_desc, cron_job_config, attachment_data)
    scheduler.add_task(task)


def delete_task(task_id):
    scheduler.delete_task(task_id)


def get_task_list():
    return scheduler.get_task_list()


def reset_task(task_id):
    scheduler.reset_task(task_id)
    ctrl = U2AndroidController()
    ctrl.init_env()
    ctrl.click_by_point(ESCAPE)
