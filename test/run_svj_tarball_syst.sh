#!/bin/bash -e

export DO_MG_SYSTEMATICS=true
COMMAND_NAME=$(echo $0 | sed 's/_syst.sh/.sh/')
$COMMAND_NAME "$@"
