import { Component, OnInit } from '@angular/core';
import { ProcStatusService } from '../../services/proc_status.service';
import { ProcLog } from 'src/app/date/IProcLog';
import { ActivatedRoute } from '@angular/router';
import Swal from 'sweetalert2';

@Component({
    selector: 'app-proc',
    templateUrl: './proc.page.component.html',
})
export class ProcComponent implements OnInit {
    procLogs: ProcLog[]

    procLogCurrent: ProcLog

    constructor(private procStatus: ProcStatusService, private activatedRoute: ActivatedRoute) {

    }
    
    ngOnInit(): void {
        this.procStatus.getTaskStatuses().subscribe((res: any) => {
            this.procLogs = res;
        });

        this.activatedRoute.queryParams.subscribe(params => {
            const proc_id = params['proc_id'];
            this.openProcLog(proc_id);
            console.log(proc_id);
        });
    }

    openProcLog(proc_id: number) {
        this.procStatus.getTaskStatus(proc_id).subscribe((res: any) => {
            this.procLogCurrent = res;
            console.log(res)
        })
    }
}
