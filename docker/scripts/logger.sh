. /scripts/helpers.sh
. /scripts/colors.sh

get_color_for_log_level() {
  case $1 in
    info)
      printf "${color_info}"
      ;;
    debug)
      printf "${color_debug}"
      ;;
    success)
      printf "${color_success}"
      ;;
    error)
      printf "${color_error}"
      ;;
    white)
      printf "${color_white}"
      ;;
    *)
      printf "${color_reset}"
      ;;
  esac
}

get_log_level_text_part() {
  case $1 in
    info)
      printf "| INFO     |"
      ;;
    debug)
      printf "| DEBUG    |"
      ;;
    success)
      printf "| SUCCESS  |"
      ;;
    error)
      printf "| ERROR    |"
      ;;
    *)
      printf ""
      ;;
  esac
}

log() (
  log_level=$1
  text=$2

  text_color=$(get_color_for_log_level "${log_level}")
  log_level_text=$(get_log_level_text_part "${log_level}")
  current_time=$(date +"%Y-%m-%d %H:%M:%S.%3N")

  echo "${text_color}${current_time} ${log_level_text} ${color_reset}${text}${color_reset}"
)

log_debug() (
  text=$1
  log "debug" "${text}"
)

log_info() (
  text=$1
  log "info" "${text}"
)

log_success() (
  text=$1
  log "success" "${text}"
)

log_error() (
  text=$1
  log "error" "${text}"
)
