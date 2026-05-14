import { createClient } from "@supabase/supabase-js";

const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
const anon = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

// Browser-safe client. Auth is deferred — this is here for the next pass.
export const supabaseBrowser = url && anon ? createClient(url, anon) : null;
