"""Helper funcitions to generate a podman compose file."""

from collections import namedtuple

from ipalab_config.utils import die, get_hostname, is_ip_address, ensure_fqdn


# The global ip address generator.
IP_GENERATOR = iter(range(10, 255))


def get_compose_config(containers, network, distro, ips=IP_GENERATOR):
    """Create config for all containers in the list."""

    def node_dns_key(hostname):
        return hostname.replace(".", "_")

    result = {}
    if isinstance(containers, dict):
        containers = containers.get("hosts", [])
    if not containers:
        return {}, {}
    nodes = {}
    for container, ipaddr in zip(containers, ips):
        name = container["name"]
        node_distro = container.get("distro", distro)
        ip_address = f"{network.subnet}.{ipaddr}"
        hostname = get_hostname(container, name, network.domain)
        effective_dns = container.get("dns", network.dns)
        if effective_dns and not (
            is_ip_address(effective_dns) or "{" in effective_dns
        ):
            effective_dns = "{{{0}}}".format(
                ensure_fqdn(effective_dns, network.domain)
            )
        nodes[node_dns_key(hostname)] = ip_address
        config = {
            "container_name": name,
            "systemd": True,
            "no_hosts": True,
            "restart": "never",
            "cap_add": ["SYS_ADMIN"],
            "security_opt": ["label:disable"],
            "hostname": hostname,
            "networks": {network.networkname: {"ipv4_address": ip_address}},
            "image": f"localhost/{node_distro}",
            "build": {
                "context": "containerfiles",
                "dockerfile": f"{node_distro}",
            },
        }
        if effective_dns:
            config["dns"] = node_dns_key(effective_dns)
            config["dns_search"] = network.domain
        result[name] = config
    return nodes, result


def compose_servers(servers, network):
    """Generate service compose configuration for IPA servers."""
    return get_compose_config(servers, network)


def compose_clients(clients, network):
    """Generate service compose configuration for IPA clents."""
    return get_compose_config(clients, network)


def gen_compose_data(lab_config, subnet):
    """Generate podamn compose file based on provided configuration."""
    Network = namedtuple("Network", ["domain", "networkname", "subnet", "dns"])
    labname = lab_config.get("lab_name", "ipa-lab")
    config = {"name": labname}
    networkname = f"ipanet-{labname}"
    config["networks"] = {
        networkname: {
            "driver": "bridge",
            "ipam": {
                "config": [
                    {
                        "subnet": f"{subnet}.0/24",
                        "gateway": f"{subnet}.1",
                    }
                ]
            },
        }
    }
    services = config.setdefault("services", {})

    ipa_deployments = lab_config.get("ipa_deployments")
    deployment_dns = []
    for deployment in ipa_deployments:
        domain = deployment.get("domain", "ipa.test")
        distro = deployment.get("distro", "fedora-latest")
        dns = deployment.get("dns")
        if dns and not is_ip_address(dns):
            dns = "{{{0}}}".format(ensure_fqdn(dns, domain))
        network = Network(domain, networkname, subnet, dns)
        cluster_config = deployment.get("cluster")
        if not cluster_config:
            die(f"Cluster not defined for domain '{domain}'")
        nodes = {}
        # Get servers configurations
        servers = cluster_config.get("servers")
        if servers:
            # First server must not have 'dns' set
            ips, servers_cfg = get_compose_config([servers[0]], network, distro)
            deployment_dns.append(next(iter(ips.values())))
            first_server_data = next(iter(servers_cfg.values()))
            first_server_data.pop("dns", None)
            services.update(servers_cfg)
            nodes.update(ips)
            # Replicas may have all settings
            ips, servers_cfg = get_compose_config(servers[1:], network, distro)
            services.update(servers_cfg)
            nodes.update(ips)
        else:
            print(f"Warning: No servers defined for domain '{domain}'")
            deployment_dns.append(None)
        # Get clients configuration
        clients = cluster_config.get("clients")
        ips, clients_cfg = get_compose_config(clients, network, distro)
        services.update(clients_cfg)
        nodes.update(ips)
        # We must have at lest one node at the end.
        if not nodes:
            die("At least one server or client must be defined for {domain}.")
        # Update 'dns' on each service
        for service in services.values():
            if "dns" in service:
                service["dns"] = service["dns"].format(**nodes)

    return config, deployment_dns
