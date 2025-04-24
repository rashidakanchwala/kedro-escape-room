from kedro.framework.hooks import hook_impl
from kedro.config import OmegaConfigLoader
from pathlib import Path
import hashlib

class InvisibleGatekeeperHook:
    @hook_impl
    def before_node_run(self, node, inputs, is_async, session_id):
        if node.name != "reporting.decode_final_clue_node":
            return

        conf_loader = OmegaConfigLoader(conf_source=str(Path.cwd() / "conf"))
        creds = conf_loader.get("credentials") or {}
        author = creds.get("quoted_by", "").strip().lower()

        expected = "0728c3bde7535df1df6e6a415541dee3924413d4421074273a558a4dd5f87dab"

        if hashlib.sha256(author.encode()).hexdigest() != expected:
            raise ValueError(
                "“Vulnerability is the birthplace of innovation, creativity, and change.”"
            )
