## Script (Python) "getFolderContents"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=contentFilter=None,batch=False,b_size=100,full_objects=False
##title=wrapper method around to use catalog to get folder contents
##

catalog = context.portal_catalog.aq_inner
mtool = context.portal_membership
cur_path = '/'.join(context.getPhysicalPath())
path = {}

if not contentFilter:
    contentFilter=dict(context.REQUEST)
    # The form is what really matters
    contentFilter.update(dict(getattr(context.REQUEST, 'form',{})))
else:
    contentFilter = dict(contentFilter)

if not contentFilter.get('sort_on', None):
    contentFilter['sort_on'] = 'getObjPositionInParent'

if contentFilter.get('path', None) is None:
    path['query'] = cur_path
    path['depth'] = 1
    contentFilter['path'] = path

show_inactive = mtool.checkPermission('Access inactive portal content', context)

contents = catalog.queryCatalog(contentFilter, show_all=1, show_inactive=show_inactive)

if full_objects:
    contents = [b.getObject() for b in contents]

if batch:
    from Products.CMFPlone import Batch
    b_start = context.REQUEST.get('b_start', 0)
    batch = Batch(contents, b_size, int(b_start), orphan=0)
    return batch

return contents