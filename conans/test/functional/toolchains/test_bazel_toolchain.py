import json
import textwrap

from conans.test.assets.genconanfile import GenConanfile
from conans.test.utils.tools import TestClient


def test_toolchain_empty_config():
    client = TestClient(path_with_spaces=False)

    conanfile = GenConanfile().with_settings("os", "compiler", "build_type", "arch").\
        with_generator("BazelToolchain")

    client.save({"conanfile.py": conanfile})
    client.run("install .")

    config = json.loads(client.load("conanbuild.json"))

    assert config['bazel_config'] is None
    assert config['bazelrc_path'] is None


def test_toolchain_loads_config_from_profile():
    client = TestClient(path_with_spaces=False)

    profile = textwrap.dedent("""
    include(default)
    [conf]
    tools.google.bazel:config=test_config
    tools.google.bazel:bazelrc_path=/path/to/bazelrc
    """)

    conanfile = GenConanfile().with_settings("os", "compiler", "build_type", "arch").\
        with_generator("BazelToolchain")

    client.save({
        "conanfile.py": conanfile,
        "test_profile": profile
    })
    client.run("install . -pr=test_profile")

    config = json.loads(client.load("conanbuild.json"))

    assert config['bazel_config'] == "test_config"
    assert config['bazelrc_path'] == "/path/to/bazelrc"
