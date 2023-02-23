import { Component, Input, OnInit } from '@angular/core';
import { ProcStatusService } from '../../services/proc_status.service';
import { InitFile as data } from '../../date/initfile';
import { ModalService } from 'src/app/components/modal/modalService';
import { IInitFile } from 'src/app/date/IInitfile';
import { HttpErrorResponse } from '@angular/common/http';
import { catchError, throwError } from 'rxjs';
import { ProcLog } from 'src/app/date/IProcLog';
import { Router, ActivatedRoute, Params } from '@angular/router';

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
        })
    }
}
