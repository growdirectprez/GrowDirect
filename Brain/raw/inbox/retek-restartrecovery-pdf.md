---
date: 2026-04-24
type: raw
source: Brain/raw/.extract/Other Retek Decks/Retek RestartRecovery.pdf.md
tags: [retail, retek, rms, rib, rdm, 2003-2005]
project: retail
status: unprocessed
---

# Retek RestartRecovery.pdf

## Source
File: `Brain/raw/.extract/Other Retek Decks/Retek RestartRecovery.pdf.md`
Size: 6,970 bytes

## Raw content
Restart and Recovery

Retek has implemented a restart recovery process in its batch architecture.  The general purpose of the
restart/recovery is three-fold:

Recover a halted process from the point of failure,
Prevent system halts due to large numbers of transactions,
Allow multiple instances of a given process to be active at the same time.

Further, the RMS restart/recovery tracks batch execution statistics and does not require DBA authority to
execute.

The restart capabilities will revolve around a program’s logical unit of work (LUW).  A batch program will
process transactions and commit points will be enabled based on the LUW.   LUWs will consist of a
relatively unique transaction key (such as sku/store) and a maximum commit counter.  Commit events will
take place after the number of processed transaction keys meets or exceeds the maximum commit counter,
e.g. every 10,000 sku/store combinations a commit will occur.   At the time of the commit, key data
information that is necessary for restart is stored in the restart tables.  In the event of a handled or un-
handled exception, transactions will be rolled back to the last commit point, and upon restart the key
information will be retrieved from the tables so that processing can continue from the last commit point.

Diagram 1 – Restart/recovery table relationships

restart control
(PK) program_name
program_ desc
driver_name
num_threads
update_allowed
process_flag
commit_max_ ctr

restart program history
restart_name
thread_ val
start_time
program_name
commit_
restart_time
finish_time

maz_

ctr

restart program status
(PK) restart_name
(PK) thread_ val
start_time
program_name
program_status
restart_flag
restart_time
finish_time
current_
pid
current_operator_id
err_message

restart bookmark
restart_name
thread_ val
bookmark_string
application_image

restart view
driver_name
num_threads
driver_value
thread_ val

Table & File-Based Restart/Recovery
The restart/recovery process works by storing all the data necessary to resume processing from the last
commit point. Therefore, the necessary information will be updated on the restart_bookmark table before
the processed data is committed.  Query-based and file-based modules will store different information on
the restart tables, and will therefore call different functions within the restart/recovery API to perform their
tasks.

When a program's process is query-based, i.e. a module is driven by a driving query that processes the
retrieved rows, then the information that is stored on the restart_bookmark table is related to the data
retrieved in the driving query.  If the program fails while processing, the information that is stored on the
restart-tables can be used in the conditional where-clause of the driving query to only retrieve data that has
yet to be processed since the last commit event.

Retek Confidential

1

File-based processing, however, simply needs to store the file location at the time of the last commit point.
This file's byte location is stored on the restart_bookmark table and will be retrieved at the time of a restart.
This location information will be used to seek forward in the re-opened file to the point at which the data
was last commited.

Because there is different information being saved to and retrieved from  the restart_bookmark table for
each of the different types of processing, different functions will need to be called to perform the
restart/recovery logic.  The query-based processing will call the restart_init and restart_commit functions
while the file-based processing will call the restart_file_init and restart_file_commit functions.

In addition to the differences in API function calls, the batch processing flow of the restart/recovery will
differ between the files.  Table-based restart/recovery will need to use a priming fetch logical flow, while
the file-based processing will usually read lines in a batch.  Table-based processing requires its structure to
ensure that the LUW key has changed before a commit event can be allowed to occur, while the file-based
processing does not need to evaluate the LUW, which can typically be thought of the type of transaction
being processed by the input file.

Diagram 2 - Table-Based Restart/Recovery Program Flow

Initialization Logic
(call restart_init)

Process Function

Priming fetch

Process

Fetch

Commit

Close Logic

Retek Confidential

2

Diagram 3 - File-Based Restart/Recovery Program Flow

Initialization Logic
(call restart_init)

File Open & Seek

Outer Loop
feed multiple records into buffer

Inner Loop
process individual records

Process

End Inner Loop

Commit

End Outer Loop

Close Logic

Multi-Threading

Processing multiple instances of a given program can be accomplished through “threading”.  This requires
driving cursors to be separated into discrete segments of data to be processed by different threads.  This
will be accomplished through stored procedures that will separate threading mechanisms (e.g. departments
or stores) into particular threads given value (e.g. department 1001) and the total number of threads for a
given process.

File-based processing will not truly "thread" its processing. The same data file will never be acted upon by
multiple processes, however, Multi-threading will be accomplished by dividing the data into separate files
each of which will be acted upon by a separate process.   The thread value is related to the input file. This is
necessary to ensure that the appropriate information can be tied back to the relevant file in the event of a
restart.

Query-based Commit
Thresholds

The restart capabilities revolve around a program’s logical unit of work (LUW).  A batch program
processes transactions and commit points are enabled based on the LUW.   An LUW is comprised of a
transaction key (such as sku/store) and a maximum commit counter.  Commit events occur when after a

Retek Confidential

3

given number of transaction keys are processed.   At the time of the commit, key data information that is
necessary for restart is stored in the restart table.  In the event of a handled or un-handled exception,
transactions will be rolled back to the last commit point.  Upon restart the restart key information will be
retrieved from the tables so that processing can resume with the unprocessed data.

Array Processing

Retek batch architecture uses array processing to improve performance wherever possible.   Instead of
processing SQL statements using scalar data, data is grouped into arrays and used as bind variables in SQL
statements.  This improves performance by reducing the server/client and network traffic.

Array processing is used for select, insert, delete and update statements.   Retek typically will not statically
define the array sizes, but will use the restart maximum commit variable as a sizing multiple.  Users should
keep this in mind when defining the system's maximum commit counters.

Retek Confidential

4


## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
