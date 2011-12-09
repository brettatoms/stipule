usage = """setup.py <command>
  - upload: upload new data files
  - deploy: update application at appengine server
  - clear_datastore: clear the production datastore
"""

if __name__ == '__main__':
    actions = {'upload': upload,
               'deploy': deploy,
               'update': deploy,
               'clear_datastore': clear_datastore}

    if len(sys.argv) < 2 or sys.argv[1] not in actions:
        print usage
        sys.exit(1)
    
    actions[sys.argv[1]]()
