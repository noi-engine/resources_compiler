find_package(Python3 REQUIRED COMPONENTS Interpreter)

set(RESOURCES_PACKER_DIR "${CMAKE_CURRENT_LIST_DIR}")
set(RESOURCES_PACKER_VENV "${CMAKE_BINARY_DIR}/.venv_resources_compiler")

if(WIN32)
    set(RESOURCES_PACKER_PYTHON "${RESOURCES_PACKER_VENV}/Scripts/python.exe")
else()
    set(RESOURCES_PACKER_PYTHON "${RESOURCES_PACKER_VENV}/bin/python")
endif()

function(_setup_resources_compiler_env)
    if(NOT EXISTS "${RESOURCES_PACKER_PYTHON}")
        message(STATUS "[Resource Packer] Creating virtual environment: ${RESOURCES_PACKER_VENV}")
        execute_process(
                COMMAND ${Python3_EXECUTABLE} -m venv "${RESOURCES_PACKER_VENV}"
                COMMAND_ECHO STDOUT
                RESULT_VARIABLE VENV_RES
                ERROR_VARIABLE VENV_ERR
        )
        if(NOT VENV_RES EQUAL 0)
            message(FATAL_ERROR "[Resource Packer ERROR] Failed to create venv:\n${VENV_ERR}")
        endif()
    endif()

    set(REQ_FILE "${RESOURCES_PACKER_DIR}/requirements.txt")
    if(EXISTS "${REQ_FILE}")
        message(STATUS "[Resource Packer] Installing pip requirements with VERBOSE output...")
        execute_process(
                COMMAND "${RESOURCES_PACKER_PYTHON}" -m pip install -r "${REQ_FILE}" --verbose
                COMMAND_ECHO STDOUT
                RESULT_VARIABLE PIP_RES
                ERROR_VARIABLE PIP_ERR
        )
        if(NOT PIP_RES EQUAL 0)
            message(FATAL_ERROR "[Resource Packer ERROR] Failed to install requirements:\n${PIP_ERR}")
        endif()
    endif()
endfunction()

_setup_resources_compiler_env()

function(compile_resources INPUT_FOLDER OUTPUT_PACK_FILE)
    if(ARGV2)
        set(TARGET_NAME "${ARGV2}")
    else()
        string(MAKE_C_IDENTIFIER "pack_resources_${INPUT_FOLDER}" TARGET_NAME)
    endif()

    add_custom_target(${TARGET_NAME} ALL
            COMMAND "${RESOURCES_PACKER_PYTHON}" "${RESOURCES_PACKER_DIR}/scripts/main.py"
            --input "${INPUT_FOLDER}"
            --output "${OUTPUT_PACK_FILE}"
            WORKING_DIRECTORY "${RESOURCES_PACKER_DIR}"
            COMMENT "[Resource Packer] Compiling resources into package: ${OUTPUT_PACK_FILE}"
            USES_TERMINAL
    )
endfunction()