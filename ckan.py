"""Small client for the CalHHS open data portal, shared by the helper scripts.

It mirrors what the dashboard (docs/index.html) does: it finds the dataset's
CSV resource that has a live datastore via package_show, and it pages
through datastore_search, which returns at most 50,000 rows per request.
"""
import requests

API_BASE = 'https://data.chhs.ca.gov/api/3/action'
PACKAGE_ID = 'wastewater-surveillance-data-california'
FALLBACK_RESOURCE_ID = '2742b824-3736-4292-90a9-7fad98e94c06'
TIMEOUT = 60        # seconds per request
PAGE_SIZE = 50000   # the portal's cap on rows per response


class CkanError(Exception):
    """The portal answered, but not with a successful result."""


def call(action, **params):
    """Call a CKAN action and return its `result`."""
    r = requests.get(f"{API_BASE}/{action}", params=params, timeout=TIMEOUT)
    try:
        data = r.json()
    except ValueError:
        raise CkanError(f"HTTP {r.status_code}: response is not JSON")
    if not data.get('success'):
        raise CkanError(data.get('error'))
    return data['result']


def resource_id():
    """The dataset's CSV resource with a live datastore, as the dashboard picks it."""
    try:
        package = call('package_show', id=PACKAGE_ID)
    except (requests.RequestException, CkanError) as e:
        print(f"package_show failed ({e}); using the fallback resource id.")
        return FALLBACK_RESOURCE_ID
    for r in package.get('resources', []):
        if (r.get('format') == 'CSV' and 'Wastewater Surveillance' in (r.get('name') or '')
                and r.get('datastore_active')):
            return r['id']
    return FALLBACK_RESOURCE_ID


def search(query, fields=None, resource=None):
    """Every row matching full-text `query`, paged past the per-response cap.

    Pages are sorted by _id so they don't overlap; if the total changes
    between pages (the table was reloaded), the search starts over.
    `fields` limits the columns returned.
    """
    params = {'resource_id': resource or resource_id(), 'q': query, 'sort': '_id', 'limit': PAGE_SIZE}
    if fields:
        params['fields'] = ','.join(fields)
    for _ in range(2):
        records, total = [], None
        while total is None or len(records) < total:
            result = call('datastore_search', offset=len(records), **params)
            if total is None:
                total = result['total']
            elif result['total'] != total:
                break  # reloaded between pages: start over
            if not result['records'] and len(records) < total:
                break  # rows missing: start over
            records.extend(result['records'])
        else:
            return records
    raise CkanError('the dataset changed while it was being read; try again')
