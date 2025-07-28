from fastmcp import FastMCP
from .approval_security import mcp as approval_security_server
from .dapp_security import mcp as dapp_security_server
from .malicious_address import mcp as malicious_address_server
from .nft_security import mcp as nft_security_server
from .phishing_site import mcp as phishing_site_server
from .rug_pull_detection import mcp as rug_pull_detection_server
# from .signature_data_decode import mcp as signature_data_decode_server
from .supported_chains import mcp as supported_chains_server
from .token_security import mcp as token_security_server

mcp_server = FastMCP("GoPlusLabsServer")
mcp_server.mount(approval_security_server, "ApprovalSecurity")
mcp_server.mount(dapp_security_server, "DappSecurity")
mcp_server.mount(malicious_address_server, "MaliciousAddress")
mcp_server.mount(nft_security_server, "NftSecurity")
mcp_server.mount(phishing_site_server, "PhishingSite")
mcp_server.mount(rug_pull_detection_server, "RugPullDetection")
mcp_server.mount(supported_chains_server, "SupportedChains")
mcp_server.mount(token_security_server, "TokenSecurity")

if __name__ == "__main__":
    # mcp_server.run(host='0.0.0.0', port=8000)
    mcp_server.run()