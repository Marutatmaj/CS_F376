/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

const bit<16> TYPE_IPV4 = 0x800;
const bit<16> TYPE_TIME = 0x900; 

/*************************************************************************
*********************** H E A D E R S  ***********************************
*************************************************************************/

typedef bit<9>  egressSpec_t;
typedef bit<48> macAddr_t;
typedef bit<32> ip4Addr_t;

header ethernet_t {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
}

header ipv4_t {
    bit<4>    version;
    bit<4>    ihl;
    bit<8>    diffserv;
    bit<16>   totalLen;
    bit<16>   identification;
    bit<3>    flags;
    bit<13>   fragOffset;
    bit<8>    ttl;
    bit<8>    protocol;
    bit<16>   hdrChecksum;
    ip4Addr_t srcAddr;
    ip4Addr_t dstAddr;
}

header time_t {
    bit<16> proto_id;
    bit<48> time;
}

struct metadata {
    // No metadata needed for basic IPv4 forwarding
    bit<19> queue_size;
    bit<48> cur_persist_time;
}

struct headers {
    ethernet_t ethernet;
    ipv4_t     ipv4;
    time_t     time;
}

/*************************************************************************
*********************** P A R S E R  ***********************************
*************************************************************************/

parser MyParser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {

    state start {
        transition parse_ethernet;
    }

    state parse_ethernet {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            TYPE_IPV4: parse_ipv4;    
            default: accept;
        }
    }

    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        transition parse_time;
    }

    state parse_time {
        packet.extract(hdr.time);
        transition accept;
    }
}


/*************************************************************************
************   C H E C K S U M    V E R I F I C A T I O N   *************
*************************************************************************/

control MyVerifyChecksum(inout headers hdr, inout metadata meta) {
    apply { }
}

/*************************************************************************
**************  I N G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata) {
                    
    direct_counter(CounterType.packets_and_bytes) direct_port_counter;

    action drop() {
        mark_to_drop(standard_metadata);
    }

    action ipv4_forward(macAddr_t dstAddr, egressSpec_t port) {
        hdr.ethernet.srcAddr = hdr.ethernet.dstAddr;
        hdr.ethernet.dstAddr = dstAddr;
        standard_metadata.egress_spec = port;
        hdr.ipv4.ttl = hdr.ipv4.ttl - 1;
    }

    table ipv4_lpm {
        key = {
            hdr.ipv4.dstAddr: lpm;
        }
        actions = {
            ipv4_forward;
            drop;
        }
        default_action = drop;
        counters = direct_port_counter;
        size = 128;
    }

    table debug_table {
        key = {
            hdr.ipv4.identification: exact;
            hdr.ipv4.ttl: exact;
            hdr.ethernet.dstAddr: exact;
            standard_metadata.deq_qdepth: exact;
            hdr.time.proto_id: exact;
            hdr.time.time: exact;
            meta.queue_size: exact;
        }
        actions = { NoAction; }
        const default_action = NoAction();
    }

    apply {
        if (meta.queue_size < standard_metadata.deq_qdepth && meta.queue_size > 0) {
            mark_to_drop(standard_metadata);
        }

        if (hdr.ipv4.isValid()) {
            hdr.ipv4.dstAddr = 0x0a020302;
            ipv4_lpm.apply();
        }
    }
}

/*************************************************************************
****************  E G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyEgress(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {
    
    table debug_table {
        key = {
            hdr.ipv4.identification: exact;
            hdr.ipv4.ttl: exact;
            hdr.ethernet.dstAddr: exact;
            standard_metadata.deq_qdepth: exact;
            hdr.time.proto_id: exact;
            hdr.time.time: exact;
            meta.queue_size: exact;
            meta.cur_persist_time: exact;
        }
        actions = { NoAction; }
        const default_action = NoAction();
    }
                    
    apply {
        if (!hdr.time.isValid()) {
            hdr.time.setValid();
            hdr.time.proto_id = TYPE_IPV4;
            hdr.time.time = standard_metadata.egress_global_timestamp - standard_metadata.ingress_global_timestamp;
        }
        else{
            hdr.time.time = hdr.time.time + (standard_metadata.egress_global_timestamp - standard_metadata.ingress_global_timestamp);
            meta.queue_size = (bit<19>)(hdr.time.time / (0x40));
        }

        meta.cur_persist_time = standard_metadata.egress_global_timestamp - standard_metadata.ingress_global_timestamp;

        debug_table.apply();
    }
}

/*************************************************************************
*************   C H E C K S U M    C O M P U T A T I O N   **************
*************************************************************************/

control MyComputeChecksum(inout headers hdr, inout metadata meta) {
    apply {
        update_checksum(
            hdr.ipv4.isValid(),
            { hdr.ipv4.version,
              hdr.ipv4.ihl,
              hdr.ipv4.diffserv,
              hdr.ipv4.totalLen,
              hdr.ipv4.identification,
              hdr.ipv4.flags,
              hdr.ipv4.fragOffset,
              hdr.ipv4.ttl,
              hdr.ipv4.protocol,
              hdr.ipv4.srcAddr,
              hdr.ipv4.dstAddr },
            hdr.ipv4.hdrChecksum,
            HashAlgorithm.csum16);
    }
}

/*************************************************************************
***********************  D E P A R S E R  *******************************
*************************************************************************/

control MyDeparser(packet_out packet, in headers hdr) {
    apply {
        packet.emit(hdr.ethernet);
        packet.emit(hdr.time);
        packet.emit(hdr.ipv4);
    }
}

/*************************************************************************
***********************  S W I T C H  *******************************
*************************************************************************/

V1Switch(
    MyParser(),
    MyVerifyChecksum(),
    MyIngress(),
    MyEgress(),
    MyComputeChecksum(),
    MyDeparser()
) main;