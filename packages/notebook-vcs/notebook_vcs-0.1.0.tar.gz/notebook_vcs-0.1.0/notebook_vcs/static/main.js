define([
    'base/js/namespace',
    'base/js/dialog',
    'jquery'
], function(Jupyter, dialog, $) {
    'use strict';

    class NotebookVCS {
        constructor() {
            this.baseUrl = Jupyter.notebook.base_url;
            this.setupToolbar();
            this.setupEventHandlers();
        }

        setupToolbar() {
            // Add VCS toolbar
            const vcsGroup = $('<div/>')
                .addClass('btn-group')
                .attr('id', 'vcs-toolbar');

            // Commit button
            $('<button/>')
                .addClass('btn btn-default')
                .attr('title', 'Commit current notebook state')
                .append('<i class="fa fa-save"></i> Commit')
                .click(() => this.showCommitDialog())
                .appendTo(vcsGroup);

            // Branch button
            $('<button/>')
                .addClass('btn btn-default')
                .attr('title', 'Branch operations')
                .append('<i class="fa fa-code-fork"></i> Branch')
                .click(() => this.showBranchDialog())
                .appendTo(vcsGroup);

            // History button
            $('<button/>')
                .addClass('btn btn-default')
                .attr('title', 'View history')
                .append('<i class="fa fa-history"></i> History')
                .click(() => this.showHistoryDialog())
                .appendTo(vcsGroup);

            // Add the toolbar group
            $('#maintoolbar-container').append(vcsGroup);
        }

        setupEventHandlers() {
            // Add event handlers for notebook events
            Jupyter.notebook.events.on('kernel_ready.Kernel', () => {
                console.log('Kernel is ready');
                this.initializeVCS();
            });
        }

        initializeVCS() {
            // Initialize VCS when kernel is ready
            $.ajax({
                url: this.baseUrl + 'vcs/init',
                method: 'POST',
                contentType: 'application/json',
                success: (data) => {
                    console.log('VCS initialized:', data);
                },
                error: (jqXHR, textStatus, errorThrown) => {
                    console.error('Failed to initialize VCS:', errorThrown);
                }
            });
        }

        showCommitDialog() {
            const form = $('<div/>').addClass('form-group');
            
            const input = $('<input/>')
                .attr('type', 'text')
                .addClass('form-control')
                .attr('placeholder', 'Enter commit message');
                
            form.append(input);

            dialog.modal({
                title: 'Create Commit',
                body: form,
                buttons: {
                    'Commit': {
                        class: 'btn-primary',
                        click: () => this.createCommit(input.val())
                    },
                    'Cancel': {}
                }
            });
        }

        createCommit(message) {
            $.ajax({
                url: this.baseUrl + 'vcs/commit',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ message: message }),
                success: (data) => {
                    if (data.status === 'success') {
                        dialog.modal({
                            title: 'Success',
                            body: `Created commit: ${data.commit_hash}`,
                            buttons: { 'OK': {} }
                        });
                    }
                },
                error: (jqXHR, textStatus, errorThrown) => {
                    dialog.modal({
                        title: 'Error',
                        body: `Failed to create commit: ${errorThrown}`,
                        buttons: { 'OK': {} }
                    });
                }
            });
        }

        showBranchDialog() {
            $.ajax({
                url: this.baseUrl + 'vcs/branch',
                method: 'GET',
                success: (data) => {
                    if (data.status === 'success') {
                        this.renderBranchDialog(data.branches);
                    }
                },
                error: (jqXHR, textStatus, errorThrown) => {
                    console.error('Failed to get branches:', errorThrown);
                }
            });
        }

        renderBranchDialog(branches) {
            const container = $('<div/>');
            
            // Branch list
            const list = $('<ul/>').addClass('list-group');
            branches.forEach(branch => {
                const item = $('<li/>')
                    .addClass('list-group-item')
                    .append(
                        $('<span/>').text(branch.name),
                        $('<small/>').addClass('text-muted ml-2').text(branch.head.substr(0, 8))
                    )
                    .click(() => this.switchBranch(branch.name));
                list.append(item);
            });
            
            // New branch form
            const form = $('<div/>').addClass('form-group mt-3');
            const input = $('<input/>')
                .attr('type', 'text')
                .addClass('form-control')
                .attr('placeholder', 'New branch name');
            form.append(input);
            
            container.append(list, form);

            dialog.modal({
                title: 'Branch Operations',
                body: container,
                buttons: {
                    'Create Branch': {
                        class: 'btn-primary',
                        click: () => this.createBranch(input.val())
                    },
                    'Close': {}
                }
            });
        }

        createBranch(branchName) {
            $.ajax({
                url: this.baseUrl + 'vcs/branch',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    action: 'create',
                    branch_name: branchName
                }),
                success: (data) => {
                    if (data.status === 'success') {
                        this.showBranchDialog();  // Refresh the dialog
                    }
                },
                error: (jqXHR, textStatus, errorThrown) => {
                    console.error('Failed to create branch:', errorThrown);
                }
            });
        }

        switchBranch(branchName) {
            $.ajax({
                url: this.baseUrl + 'vcs/branch',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    action: 'switch',
                    branch_name: branchName
                }),
                success: (data) => {
                    if (data.status === 'success') {
                        location.reload();  // Reload notebook with new branch
                    }
                },
                error: (jqXHR, textStatus, errorThrown) => {
                    console.error('Failed to switch branch:', errorThrown);
                }
            });
        }

        showHistoryDialog() {
            $.ajax({
                url: this.baseUrl + 'vcs/history',
                method: 'GET',
                success: (data) => {
                    if (data.status === 'success') {
                        this.renderHistoryDialog(data.history);
                    }
                },
                error: (jqXHR, textStatus, errorThrown) => {
                    console.error('Failed to get history:', errorThrown);
                }
            });
        }

        renderHistoryDialog(history) {
            const container = $('<div/>');
            
            // History list
            const list = $('<ul/>').addClass('list-group');
            history.forEach(commit => {
                const item = $('<li/>')
                    .addClass('list-group-item')
                    .append(
                        $('<div/>').addClass('d-flex justify-content-between')
                            .append(
                                $('<span/>').text(commit.message || 'No message'),
                                $('<small/>').addClass('text-muted').text(commit.hash.substr(0, 8))
                            ),
                        $('<small/>').addClass('text-muted d-block').text(new Date(commit.timestamp * 1000).toLocaleString())
                    )
                    .click(() => this.showRevertDialog(commit));
                list.append(item);
            });
            
            container.append(list);

            dialog.modal({
                title: 'Commit History',
                body: container,
                buttons: { 'Close': {} }
            });
        }

        showRevertDialog(commit) {
            dialog.modal({
                title: 'Revert to Commit',
                body: `Are you sure you want to revert to commit ${commit.hash.substr(0, 8)}?`,
                buttons: {
                    'Revert': {
                        class: 'btn-warning',
                        click: () => this.revertToCommit(commit.hash)
                    },
                    'Cancel': {}
                }
            });
        }

        revertToCommit(commitHash) {
            $.ajax({
                url: this.baseUrl + 'vcs/revert',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ commit_hash: commitHash }),
                success: (data) => {
                    if (data.status === 'success') {
                        location.reload();  // Reload notebook with reverted state
                    }
                },
                error: (jqXHR, textStatus, errorThrown) => {
                    console.error('Failed to revert:', errorThrown);
                }
            });
        }
    }

    // Extension initialization function
    function load_ipython_extension() {
        console.log('Loading Notebook VCS extension...');
        return new Promise((resolve) => {
            require(['notebook/js/codecell'], () => {
                const vcs = new NotebookVCS();
                console.log('Notebook VCS extension loaded successfully');
                resolve();
            });
        });
    }

    return {
        load_ipython_extension: load_ipython_extension
    };
}); 