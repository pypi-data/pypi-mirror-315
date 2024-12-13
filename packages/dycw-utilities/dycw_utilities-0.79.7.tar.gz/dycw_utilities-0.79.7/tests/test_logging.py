from __future__ import annotations

from logging import DEBUG, NOTSET, FileHandler, Logger, StreamHandler, getLogger
from pathlib import Path
from typing import Any, cast

from pytest import LogCaptureFixture, mark, param, raises
from whenever import ZonedDateTime

from tests.test_traceback_funcs.one import func_one
from utilities.iterables import one
from utilities.logging import (
    GetLoggingLevelNumberError,
    LogLevel,
    _AdvancedLogRecord,
    add_filters,
    basic_config,
    get_default_logging_path,
    get_logger,
    get_logging_level_number,
    setup_logging,
    temp_handler,
    temp_logger,
)
from utilities.pytest import skipif_windows
from utilities.typing import get_args


class TestAddFilters:
    def test_main(self) -> None:
        handler = StreamHandler()
        assert len(handler.filters) == 0
        add_filters(handler, filters=[lambda _: True])
        assert len(handler.filters) == 1

    def test_no_handlers(self) -> None:
        handler = StreamHandler()
        assert len(handler.filters) == 0
        add_filters(handler)
        assert len(handler.filters) == 0


class TestBasicConfig:
    def test_main(self) -> None:
        basic_config()
        logger = getLogger(__name__)
        logger.info("message")


class TestGetDefaultLoggingPath:
    def test_main(self) -> None:
        assert isinstance(get_default_logging_path(), Path)


class TestGetLogger:
    def test_logger(self) -> None:
        logger = getLogger(__name__)
        result = get_logger(logger)
        assert result is logger

    def test_str(self) -> None:
        result = get_logger(__name__)
        assert isinstance(result, Logger)
        assert result.name == __name__


class TestGetLoggingLevelNumber:
    @mark.parametrize(
        ("level", "expected"),
        [
            param("DEBUG", 10),
            param("INFO", 20),
            param("WARNING", 30),
            param("ERROR", 40),
            param("CRITICAL", 50),
        ],
    )
    def test_main(self, *, level: LogLevel, expected: int) -> None:
        assert get_logging_level_number(level) == expected

    def test_error(self) -> None:
        with raises(
            GetLoggingLevelNumberError, match="Invalid logging level: 'invalid'"
        ):
            _ = get_logging_level_number(cast(Any, "invalid"))


class TestLogLevel:
    def test_main(self) -> None:
        assert len(get_args(LogLevel)) == 5


class TestSetupLogging:
    @skipif_windows
    def test_main(self, *, tmp_path: Path) -> None:
        name = TestSetupLogging.test_main.__qualname__
        setup_logging(logger_name=name, files_dir=tmp_path)
        logger = getLogger(name)
        assert len(logger.handlers) == 6
        files = list(tmp_path.iterdir())
        assert len(files) == 5
        names = {f.name for f in files}
        expected = {
            ".__debug.txt.lock",
            ".__info.txt.lock",
            "debug.txt",
            "info.txt",
            "plain",
        }
        assert names == expected
        try:
            _ = func_one(1, 2, 3, 4, c=5, d=6, e=7)
        except AssertionError:
            logger.exception("message")
        assert tmp_path.joinpath("errors").is_dir()

    @skipif_windows
    def test_regular_percent_formatting(
        self, *, caplog: LogCaptureFixture, tmp_path: Path
    ) -> None:
        name = TestSetupLogging.test_regular_percent_formatting.__qualname__
        setup_logging(logger_name=name, files_dir=tmp_path)
        logger = getLogger(name)
        logger.info("int: %d, float: %.2f", 1, 12.3456)
        record = one(caplog.records)
        assert isinstance(record, _AdvancedLogRecord)
        expected = "int: 1, float: 12.35"
        assert record.message == expected

    @skipif_windows
    def test_new_brace_formatting(
        self, *, caplog: LogCaptureFixture, tmp_path: Path
    ) -> None:
        name = TestSetupLogging.test_new_brace_formatting.__qualname__
        setup_logging(logger_name=name, files_dir=tmp_path)
        logger = getLogger(name)
        logger.info("int: {:d}, float: {:.2f}, percent: {:.2%}", 1, 12.3456, 0.123456)
        record = one(caplog.records)
        assert isinstance(record, _AdvancedLogRecord)
        expected = "int: 1, float: 12.35, percent: 12.35%"
        assert record.message == expected

    @skipif_windows
    def test_no_console(self, *, tmp_path: Path) -> None:
        name = TestSetupLogging.test_no_console.__qualname__
        setup_logging(logger_name=name, console_level=None, files_dir=tmp_path)
        logger = getLogger(name)
        assert len(logger.handlers) == 5

    @skipif_windows
    def test_zoned_datetime(self, *, caplog: LogCaptureFixture, tmp_path: Path) -> None:
        name = TestSetupLogging.test_zoned_datetime.__qualname__
        setup_logging(logger_name=name, files_dir=tmp_path)
        logger = getLogger(name)
        logger.info("")
        record = one(caplog.records)
        assert isinstance(record, _AdvancedLogRecord)
        assert isinstance(record.zoned_datetime, ZonedDateTime)
        assert isinstance(record.zoned_datetime_str, str)

    @skipif_windows
    def test_extra(self, *, tmp_path: Path) -> None:
        name = TestSetupLogging.test_extra.__qualname__

        def extra(logger: Logger, /) -> None:
            handler = FileHandler(tmp_path.joinpath("extra.log"))
            handler.setLevel(DEBUG)
            logger.addHandler(handler)

        setup_logging(logger_name=name, files_dir=tmp_path, extra=extra)
        logger = getLogger(name)
        logger.info("")
        assert len(list(tmp_path.iterdir())) == 6


class TestTempHandler:
    def test_main(self) -> None:
        name = TestTempHandler.test_main.__qualname__
        logger = getLogger(name)
        logger.addHandler(h1 := StreamHandler())
        logger.addHandler(h2 := StreamHandler())
        assert len(logger.handlers) == 2
        handler = StreamHandler()
        with temp_handler(logger, handler):
            assert len(logger.handlers) == 3
        assert len(logger.handlers) == 2
        assert logger.handlers[0] is h1
        assert logger.handlers[1] is h2


class TestTempLogger:
    def test_disabled(self) -> None:
        name = TestTempLogger.test_disabled.__qualname__
        logger = getLogger(name)
        assert not logger.disabled
        with temp_logger(logger, disabled=True):
            assert logger.disabled
        assert not logger.disabled

    def test_level(self) -> None:
        name = TestTempLogger.test_level.__qualname__
        logger = getLogger(name)
        assert logger.level == NOTSET
        with temp_logger(logger, level="DEBUG"):
            assert logger.level == DEBUG
        assert logger.level == NOTSET

    def test_propagate(self) -> None:
        name = TestTempLogger.test_propagate.__qualname__
        logger = getLogger(name)
        assert logger.propagate
        with temp_logger(logger, propagate=False):
            assert not logger.propagate
        assert logger.propagate
