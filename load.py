def plugin_start3(plugin_dir):
    from neutron_router import NeutronRouterPlugin
    return NeutronRouterPlugin.start(plugin_dir)

def plugin_prefs(parent, cmdr, is_beta):
    from neutron_router import NeutronRouterPlugin
    return NeutronRouterPlugin.create_prefs(parent, cmdr, is_beta)

def journal_entry(cmdr, is_beta, system, station, entry, state):
    from neutron_router import NeutronRouterPlugin
    NeutronRouterPlugin.process_journal_entry(cmdr, is_beta, system, station, entry, state)
