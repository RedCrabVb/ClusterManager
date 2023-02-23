import { Component, Input, OnInit } from '@angular/core';
import { HostsService } from 'src/app/services/hosts.service';
import { ModalService } from 'src/app/components/modal/modalService';
import { IHost } from 'src/app/date/IHost';
import { FormControl } from '@angular/forms';
import { catchError, throwError } from 'rxjs';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
    selector: 'app-hosts',
    templateUrl: './hosts.page.html',
})
export class HostsComponent implements OnInit {
    hosts: IHost[] = [];

    hostnameModal = new FormControl('');
    usernameModal = new FormControl('');
    passwordModal = new FormControl('');

    hostnameEditModel = new FormControl('');
    usernameEditModel = new FormControl('');
    passwordEditModel = new FormControl('');

    constructor(private hostsService: HostsService, private modalService: ModalService) {

    }

    private handleError(error: HttpErrorResponse) {
        if (error.status === 0) {
            console.error('An error occurred:', error.error);
            alert('An error occurred: ' + error.message);
        } else {
            console.error(
                `Backend returned code ${error.status}, body was: `, error.error);

            alert(`Backend returned code ${error.status}, body was: ` + error.message);
        }
        return throwError(() => new Error('Something bad happened; please try again later.'));
    }

    ngOnInit(): void {
        this.hostsService.getAllHosts()
            .pipe(catchError(this.handleError))
            .subscribe((res: any) => {
                console.log(res);
                this.hosts = res;
            })
    }

    addHostModal(host: IHost) {
        this.hostnameModal.setValue(host.hostname);
        this.usernameModal.setValue(host.username);
        this.passwordModal.setValue(host.password);
    }

    getHostModal() {
        return {
            "hostname": this.hostnameModal.value,
            "username": this.usernameModal.value,
            "password": this.passwordModal.value
        }
    }

    deleteHost(host: IHost) {
        this.hostsService.deleteHost(host).subscribe((res) => {
            console.log(res);
            this.hostsService.getAllHosts().subscribe((res: any) => {
                // this.checkError(res, 'Ошибка при получении хостов');
                this.hosts = res
            })
        });

    }


    openHost(host: IHost) {
        this.hostnameEditModel.setValue(host.hostname);
        this.usernameEditModel.setValue(host.username);
        this.passwordEditModel.setValue(host.password);
        this.openModal('custom-modal-2');
    }

    addHost() {
        this.hostsService.addHosts(this.getHostModal())
            .pipe(catchError(this.handleError))
            .subscribe((res: any) => {
                alert(res.Status == 'Ok' ? 'Хост добавлен' : 'Ошибка ' + res['Status']);
                console.log(res);

                this.hostsService.getAllHosts().subscribe((res: any) => {
                    this.hosts = res

                    this.hostnameEditModel = this.hostnameModal;
                    this.usernameEditModel = this.usernameModal;
                    this.passwordEditModel = this.passwordModal;


                    this.hostnameModal = new FormControl('');
                    this.usernameModal = new FormControl('');
                    this.passwordModal = new FormControl('');

                    this.closeModal('custom-modal-1');
                    this.addHostModal(this.getHostModal());
                    this.openModal('custom-modal-2');
                })

            })
        console.log('add host')


    }

    testConnection() {
        console.log('test connection');
        const currentHost = this.getHostModal();
        this.hostsService.testConnection(currentHost)
            .pipe(catchError(this.handleError))
            .subscribe((res: any) => {
                console.log(res); alert(res.Status == true ?
                    'Соединение установлено: ' + currentHost.hostname
                    : 'Не удалось подключиться к серверу: ' + currentHost.hostname)
            })
    }


    openModal(id: string) {
        this.modalService.open(id);
    }

    closeModal(id: string) {
        this.modalService.close(id);
    }
}