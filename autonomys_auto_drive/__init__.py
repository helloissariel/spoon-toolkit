# https://mainnet.auto-drive.autonomys.xyz/api/docs
from fastmcp import FastMCP
from spoon_ai.tools.autonomys_auto_drive.subscriptions import mcp as subscriptions_server
from spoon_ai.tools.autonomys_auto_drive.objects import mcp as objects_server, mcp_management as managements_server
from spoon_ai.tools.autonomys_auto_drive.uploads import mcp as uploads_server

mcp_server = FastMCP("AutonomysAutoDriveServer")
mcp_server.mount("Subscriptions", subscriptions_server)
mcp_server.mount("Downloads", objects_server)
mcp_server.mount("Managements", managements_server)
mcp_server.mount("Uploads", uploads_server)