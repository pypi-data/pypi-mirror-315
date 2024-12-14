@rem save project path
@pushd .

@rem setup Qt
@call "%QTENV2_BAT%"

@rem restore project path (qtenv2.bat changes path to the Qt folder)
@popd

@rem setup VS2022
@call "%VCVARSALL_BAT%" %*

@rem activate the Python virtual environment, if present
@set VENV_ACTIVATE=.venv\Scripts\activate.bat
if exist %VENV_ACTIVATE% (
    @echo Activating .venv ...
    @call %VENV_ACTIVATE%
) else (
    @echo Local Python .venv not found. You can create one with "uv sync".
)

@rem start a git bash interactive session
"%GIT_BASH%" --login -i
