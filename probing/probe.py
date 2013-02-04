import requests

__all__ = ['probe_host']

# Fetches the HTTP response code for a given hostname.
# Returns -1 on connection timeout.
# Returns 703 otherwise (DNS lookup error, others).
def get_response_code(hostname, allow_redirects=False, timeout=2):
  try:
    r = requests.get(
        'http://' + hostname,
        allow_redirects=allow_redirects,
        timeout=timeout)
    return r.status_code
  except requests.exceptions.Timeout:
    return -1
  except:
    return 703

# Checks whether a connection attempt timed out as per above.
def http_status_is_timeout(status):
  return status == -1

# Checks whether a given HTTP code is a redirect.
def http_status_is_redirect(status):
  return int(status) in [301, 302]

# Checks whether a given HTTP code (or timeout) is indicative of a down server.
def http_status_is_down(status):
  status = int(status)

  if http_status_is_timeout(status) or http_status_is_fubar(status):
    return True
  if 500 <= status < 600:
    return True
  if 400 <= status < 500:
    return True
  if status in [200] or http_status_is_redirect(status):
    return False
  raise NotImplementedError('Not sure what to do with status=%d' % status)

def http_status_is_fubar(status):
  return status == 703

# Tries to fetch default HTTP page for a given host and compares it to an
# expected outcome.
# Expectations must not be contradictory.
# Returns a tuple of (expectation_matched, short_desc, long_desc).
def probe_host(hostname, should_be_down, should_redirect):
  # Check sanity of expectations.
  if should_be_down and should_redirect:
    raise UserWarning('Arguments make no sense: host cannot be both down and redirecting.')

  status = get_response_code(hostname)
  expectation_matched = False
  short_desc = ''
  details = []

  # Fill out short_desc.
  if http_status_is_fubar(status):
    short_desc = 'fubar'
  elif http_status_is_down(status):
    short_desc = 'down'
  elif http_status_is_redirect(status):
    short_desc = 'redirect'
  else:
    assert status == 200, 'Programming error: status should be 200, got %d' % status
    short_desc = 'up'

  # Describe the status and expectations.
  if http_status_is_fubar(status):
    details.append('it\'s fucked, jim')
  elif should_be_down:
    if http_status_is_down(status):
      expectation_matched = True
      if http_status_is_timeout(status):
        details.append('connection timed out')
    else:
      details.append('host expected down, got status %d' % status)
  elif should_redirect:
    if http_status_is_redirect(status):
      expectation_matched = True
      details.append('being redirected somewhere else')
    elif http_status_is_timeout(status):
      details.append('normal response expected, but request timed out')
    else:
      details.append('redirect expected, got status %d' % status)
  elif not should_be_down and not should_redirect:
    # The response must be successful.
    if status == 200:
      expectation_matched = True
      details.append('looks good from here')
    elif http_status_is_timeout(status):
      details.append('normal response expected, but request timed out')
    else:
      details.append('normal response expected, got status %d' % status)

  return (expectation_matched, short_desc, '; '.join(details))
