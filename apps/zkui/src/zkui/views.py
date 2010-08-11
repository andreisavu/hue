#  Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from desktop.lib.django_util import render
from django.http import Http404

from zkui import settings
from zkui.stats import ZooKeeperStats
from zkui.rest import ZooKeeper

def _get_global_overview():
  overview = []
  for c in settings.CLUSTERS:
    overview.append(_get_overview(c))
  return overview

def _get_overview(cluster):
  stats = {}
  for s in cluster['hostport'].split(','):
    host, port = map(str.strip, s.split(':'))

    zks = ZooKeeperStats(host, port)
    stats[s] = zks.get_stats() or {}

  cluster['stats'] = stats
  return cluster

def _group_stats_by_role(cluster):
  leader, followers = None, []
  for host, stats in cluster['stats'].items():
    stats['host'] = host

    if stats.get('zk_server_state') == 'leader':
      leader = stats

    elif stats.get('zk_server_state') == 'follower':
      followers.append(stats) 

  return leader, followers           
 
def index(request):
  overview = _get_global_overview()  
  return render('index.mako', request, 
    dict(overview=overview))

def view(request, id):
  try:
    id = int(id)
    if not (0 <= id < len(settings.CLUSTERS)):
      raise ValueError
  except (TypeError, ValueError):
    raise Http404()

  cluster = _get_overview(settings.CLUSTERS[id])
  cluster['id'] = id

  leader, followers = _group_stats_by_role(cluster)

  return render('view.mako', request, 
    dict(cluster=cluster, leader=leader, followers=followers))

def clients(request, host):
  parts = host.split(':')  
  if len(parts) != 2:
    raise Http404

  host, port = parts
  zks = ZooKeeperStats(host, port)
  clients = zks.get_clients()

  return render('clients.mako', request,
    dict(host=host, port=port, clients=clients))

def tree(request, id, path):
  try:
    id = int(id)
  except (TypeError, ValueError):
    raise Http404

  cluster = settings.CLUSTERS[id]
  cluster['id'] = id

  zk = ZooKeeper(cluster['rest_gateway'])
  znode = zk.get(path)
  children = sorted(zk.get_children_paths(path))
  
  return render('tree.mako', request,
    dict(cluster=cluster, path=path, \
      znode=znode, children=children))


def delete(request, id, path):
  try:
    id = int(id)
  except (TypeError, ValueError):
    raise Http404

  cluster = settings.CLUSTERS[id]
  cluster['id'] = id

  if request.method == 'POST':
    zk = ZooKeeper(cluster['rest_gateway'])
    try:
      zk.delete(path)
    except ZooKeeper.NotFound:
      pass

  return tree(request, id, path[:path.rindex('/')])

