from __future__ import annotations
from datetime import datetime, timedelta
from typing import Optional, List
from zoneinfo import ZoneInfo

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, JobExecutionEvent
from apscheduler.job import Job


class Scheduler:
    """
    Сервіс планування повідомлень.
    - Працює на AsyncIOScheduler
    - Зберігає задачі у SQLite через SQLAlchemyJobStore
    - Часова зона: Europe/Kyiv
    """

    def __init__(
        self,
        bot_token: str,
        *,
        sqlite_path: str = "sqlite:///jobs.sqlite",
        tz: str = "Europe/Kyiv",
        parse_mode: Optional[str] = None,
    ) -> None:
        self.bot_token = bot_token
        self.parse_mode = parse_mode
        self.tz = ZoneInfo(tz)

        self.scheduler = AsyncIOScheduler(
            timezone=self.tz,
            jobstores={"default": SQLAlchemyJobStore(url=sqlite_path)},
            executors={"default": AsyncIOExecutor()},
            job_defaults={
                "coalesce": True,
                "misfire_grace_time": 300
            },
        )

        self.scheduler.add_listener(self._on_job_executed, EVENT_JOB_EXECUTED)

    def start(self) -> None:
        """
        Запускає шедулер. Викликати один раз під час старту застосунку.
        """
        # APScheduler сам керує своїм потоком всередині asyncio-лупу
        self.scheduler.start()

    async def shutdown(self, *, wait: bool = True) -> None:
        """
        Коректно зупиняє шедулер (наприклад, при завершенні роботи бота).
        """
        self.scheduler.shutdown(wait=wait)

    async def schedule_approve(
        self,
        user_id: int,
        chat_id: int,
        seconds: int,
        *,
        job_id: Optional[str] = None,
        replace_existing: bool = True,
    ) -> Job:
        """
        Запланувати відправку повідомлення через N хвилин.
        Повертає об’єкт Job (містить .id, .next_run_time тощо).
        """

        job = self.scheduler.add_job(
            Scheduler.approve_request_job,
            trigger=IntervalTrigger(seconds=seconds),
            args=[self.bot_token, user_id, chat_id],
            kwargs={
                "run_once": True
            },
            id=job_id,
            replace_existing=replace_existing,
            max_instances=1,
        )
        return job

    async def schedule_message_once(
        self,
        chat_id: int,
        text: str,
        seconds: int,
        reply_markup = None,
        *,
        job_id: Optional[str] = None,
        replace_existing: bool = True,
    ) -> Job:
        """
        Запланувати відправку повідомлення через N хвилин.
        Повертає об’єкт Job (містить .id, .next_run_time тощо).
        """

        job = self.scheduler.add_job(
            Scheduler.send_message_job,
            trigger=IntervalTrigger(seconds=seconds),
            args=[self.bot_token, chat_id, text, self.parse_mode, reply_markup],
            kwargs={
                "run_once": True
            },
            id=job_id,
            replace_existing=replace_existing,
            max_instances=1,
        )
        return job

    async def cancel(self, job_id: str) -> bool:
        """
        Скасувати задачу за job_id. Повертає True, якщо була видалена.
        """
        job = self.scheduler.get_job(job_id)
        if job:
            job.remove()
            return True
        return False

    async def list_jobs(self) -> List[Job]:
        """Повертає список усіх джобів у шедулері."""
        return self.scheduler.get_jobs()

    @staticmethod
    async def send_message_job(bot_token: str, chat_id: int, text: str, parse_mode: Optional[str] = 'HTML', reply_markup=None, **kwargs) -> None:
        """
        Топ-рівнева корутина, яку викликає APScheduler з джобстора.
        Створює Bot на час виконання задачі, відправляє повідомлення і закриває сесію.
        """
        bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=parse_mode, link_preview_is_disabled=True))

        try:
            print(chat_id)
            await bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
        except Exception:
            pass
        finally:
            await bot.session.close()
    
    @staticmethod
    async def approve_request_job(bot_token: str, user_id: int, chat_id: int, **kwargs) -> None:
        """
        Топ-рівнева корутина, яку викликає APScheduler з джобстора.
        Створює Bot на час виконання задачі, відправляє повідомлення і закриває сесію.
        """
        bot = Bot(token=bot_token)

        try:
            await bot.approve_chat_join_request(chat_id=chat_id, user_id=user_id)
        finally:
            await bot.session.close()
    
    def _on_job_executed(self, event: JobExecutionEvent) -> None:
        job = self.scheduler.get_job(event.job_id)
        if not job:
            return
        if job.kwargs.get("run_once"):
            job.remove()
