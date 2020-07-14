## MC-QQbot

### doc

- commands should be like
    
        /command argument0 argument1 @server
        # or
        /command argument0 argument1 @serveraka
        
        # e.g.
        /whitelist add xyqyear @vanilla
        /ban xyqyear @v
        
        if there is no @ specification, then send to default server
        
- mc command modules
    
    first, permission_manager should be imported from plugin.mc, 
    and permissions needed for the plugin should be registered by:
        
        permission_manager("permission.subpermission")
    
    then, get_command and parse_response function should be provided by the module
    
    get_command function receives *session: CommandSession* and *args: str*, 
    returns (*minecraft command: str*, *permission: str*)
    
    ***the parameters used bellow may be changed in the future***
    
    parse_response function receives *permission: str* and *response: str*, 
    returns *response_parse: str*
