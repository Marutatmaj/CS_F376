#include <core.p4>
#include <v1model.p4>

control convert_error_to_bitvector(out bit<8> error_as_int,
                                   in error e)
{
    apply {
        if (e == error.NoError) {
            error_as_int = 0;
        } else if (e == error.PacketTooShort) {
            error_as_int = 1;
        } else if (e == error.NoMatch) {
            error_as_int = 2;
        } else if (e == error.StackOutOfBounds) {
            error_as_int = 3;
        } else if (e == error.HeaderTooShort) {
            error_as_int = 4;
        } else if (e == error.ParserTimeout) {
            error_as_int = 5;
        } else {
            // Unknown value
            error_as_int = 0xff;
        }
    }
}

control debug_std_meta(in standard_metadata_t standard_metadata)
{
    bit<8> parser_error_as_int;
    convert_error_to_bitvector() convert_err;
    table dbg_table {
        key = {
            // This is a complete list of fields inside of the struct
            // standard_metadata_t as of the 2021-Feb-23 version of
            // p4c in the file p4c/p4include/v1model.p4.

            // standard_metadata.parser_error is commented out because 
            // the p4c backend for bmv2 as of that date gives an error
            // if you include a field of type 'error' in a table key.
            // hdr.ipv4.ttl: exact;
            //parser_error_as_int : exact;
        }
        actions = { NoAction; }
        const default_action = NoAction();
    }
    apply {
        convert_err.apply(parser_error_as_int, standard_metadata.parser_error);
        dbg_table.apply();
    }
}
if (meta.queue_size < standard_metadata.deq_qdepth && meta.queue_size > 0) {
    mark_to_drop(standard_metadata);
}





