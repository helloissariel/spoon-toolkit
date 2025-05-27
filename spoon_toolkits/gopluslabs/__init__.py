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
mcp_server.mount("ApprovalSecurity", approval_security_server)
mcp_server.mount("DappSecurity", dapp_security_server)
mcp_server.mount("MaliciousAddress", malicious_address_server)
mcp_server.mount("NftSecurity", nft_security_server)
mcp_server.mount("PhishingSite", phishing_site_server)
mcp_server.mount("RugPullDetection", rug_pull_detection_server)
mcp_server.mount("SupportedChains", supported_chains_server)
mcp_server.mount("TokenSecurity", token_security_server)

if __name__ == "__main__":
    # mcp_server.run(host='0.0.0.0', port=8000)
    mcp_server.run()